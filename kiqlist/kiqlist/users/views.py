import hashlib
import operator
import time
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from kiqlist.goals.models import Goal
from kiqlist.notifications.utils import send_notification
from kiqlist.utils import SessionKeys
from kiqlist.utils.functions import send_noreply_mail
from kiqlist.utils.views import ajax_form_view, json_view
from kiqlist.users.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, ProfilePhotoForm
from kiqlist.users.models import ActivationKey, Profile, Follow
from kiqlist.statuses.models import Status


def register(request):
	def success(form):
		cleaned_data = form.clean()
		user = User.objects.create_user(cleaned_data.get("username"), email=cleaned_data.get("email"), password=cleaned_data.get("password"))
		user.first_name = cleaned_data.get("first_name")
		user.last_name = cleaned_data.get("last_name")
		user.is_active = False
		user.save()

		activation_key = ActivationKey(user=user, key=hashlib.md5(str(time.ctime())).hexdigest())
		activation_key.save()

		current_site = get_current_site(request)
		send_noreply_mail(
			request,
			"activation_key",
			"Activate your account on %s" % current_site.name,
			{"user": user, "activation_key": activation_key, "current_site": current_site},
			user.email
		)

	return ajax_form_view(request, RegisterForm, success, "users/register.html")


def login(request):
	def success(form):
		user = form.user
		auth_login(request, user)
		session = request.session
		session[SessionKeys.KEY_PROFILE] = Profile.objects.get(user=user)

	return ajax_form_view(request, LoginForm, success, "users/login.html")


@login_required
def edit_profile(request):
	profile = request.session[SessionKeys.KEY_PROFILE]

	def success(form):
		request.user.first_name = form.cleaned_data.get("first_name")
		request.user.last_name = form.cleaned_data.get("last_name")
		request.user.email = form.cleaned_data.get("email")
		request.user.save()

		profile.about = form.cleaned_data.get("about")
		profile.location = form.cleaned_data.get("location")
		profile.save()

		request.session.modified = True

	initial = {
		"first_name": request.user.first_name,
		"last_name": request.user.last_name,
		"email": request.user.email,
		"about": profile.about,
		"location": profile.location
	}

	return ajax_form_view(request, ProfileForm, success, "users/edit_profile_form.html",
						  initial=initial)


@login_required
def edit_password(request):
	def success(form):
		request.user.set_password(form.cleaned_data.get("password"))
		request.user.save()

	return ajax_form_view(request, ChangePasswordForm, success, "users/edit_password_form.html",
						  form_kwargs={"user": request.user})


@login_required
def edit_profile_photo(request):
	profile = request.session[SessionKeys.KEY_PROFILE]

	if request.method == "POST":
		form = ProfilePhotoForm(request.POST, request.FILES)

		if form.is_valid():
			if form.cleaned_data.get("delete"):
				profile.photo = None
				profile.save()
			elif form.cleaned_data.get("photo"):
				profile.photo = form.cleaned_data.get("photo")
				profile.save()

		request.session.modified = True
		return redirect("users.views.settings")

	else:
		form = ProfilePhotoForm()

	return render(request, "users/edit_profile_photo.html", {
		"profile": profile,
		"form": form
	})


@login_required
def logout(request):
	auth_logout(request)
	messages.success(request, "You have been logged out.")
	return redirect("home")


def activate(request, key):
	try:
		activation_key = ActivationKey.objects.get(key=key)
		activation_key.user.is_active = True
		activation_key.user.save()
		activation_key.delete()

		messages.success(request, "Your account has been activated.")
	except ObjectDoesNotExist:
		messages.success(request, "Your activation key is incorrect.")

	return redirect("home")


@login_required
def profile(request, user_pk=None):
	logged_in_user = request.user
	show_unfollow_link = False
	if not user_pk:
		user = logged_in_user
		show_follow_link = False
	else:
		user = get_object_or_404(User, pk=user_pk, is_active=True)
		show_follow_link = True
		following_users = [x.target for x in logged_in_user.following.all()]
		if user in following_users:
			show_unfollow_link = True

	profile = Profile.objects.get(user=user)

	return render(request, "users/profile.html", {
		"profile": profile,
		"show_follow_link": show_follow_link,
		"show_unfollow_link" : show_unfollow_link
	})


@login_required
def friends(request):
	following_users = [x.target for x in request.user.following.all()]
	followers_users = [x.user for x in request.user.followers.all()]
	who_to_follow_users = User.objects.filter(is_active=True). \
		exclude(pk__in=[x.pk for x in following_users] + [request.user.pk]).order_by("?").all()[:5]

	return render(request, "users/friends.html", {
		"following_users": following_users,
		"followers_users": followers_users,
		"who_to_follow_users": who_to_follow_users
	})


@login_required
def follow(request, user_pk):
	user = get_object_or_404(User, pk=user_pk)

	if Follow.objects.filter(user=request.user, target=user).count() != 0:
		return json_view(error=(1, "You are following this user."))

	Follow(user=request.user, target=user).save()
	url = reverse("kiqlist.users.views.friends") + "#followers"
	send_notification(user, "%s %s is now following you." % (request.user.first_name, request.user.last_name), url)
	return json_view()


@login_required
def unfollow(request, user_pk):
	user = get_object_or_404(User, pk=user_pk)

	try:
		follow = Follow.objects.filter(user=request.user, target=user).get()
	except Follow.DoesNotExist:
		return json_view(error=(1, "You are not following this user."))

	follow.delete()

	return json_view()


@login_required
def settings(request):
	profile = get_object_or_404(Profile, user=request.user)

	return render(request, "users/settings.html", {
		"profile": profile
	})


@login_required
def following_activity(request):
	following_users = [x.target for x in request.user.following.all()]

	activity = []

	def get_user_dict(user):
		return {
			"pk": user.pk,
			"fields": {
				"first_name": user.first_name,
				"last_name": user.last_name
			}
		}

	follows =  Follow.objects.filter(user__in=following_users).order_by("-created")[:5]
	for follow in follows:
		activity.append({
			"type": "follow",
			"data": {
				"user": get_user_dict(follow.user),
				"target": get_user_dict(follow.target)
			},
			"created": follow.created
		})

	for user in following_users:
		last_goal_queryset = Goal.objects.filter(user=user).order_by("-created")

		if len(last_goal_queryset):
			last_goal = last_goal_queryset[0]
			goal_type = "done" if last_goal.is_done else "added"
			activity.append({
				"type": goal_type,
				"data": {
					"user": get_user_dict(last_goal.user)
				},
				"created": last_goal.created
			})

	activity = sorted(activity, key=operator.itemgetter("created"), reverse=True)[:5]

	for item in activity:
		del item["created"]

	return json_view(data=activity)
