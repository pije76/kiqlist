import operator
from collections import defaultdict
from random import randrange
from urllib2 import quote

from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import GoalForm, DoneGoalForm, GoalCommentForm
from kiqlist.goals.forms import GoalTagForm
from kiqlist.hash_tags.models import extract_hash_tags
from .models import Goal, GoalImage, GoalLike, GoalRelist
from kiqlist.notifications.utils import send_notification
from kiqlist.utils.views import ajax_form_view, json_view


@login_required
def add(request):
	def success(form):
		goal = form.save(commit=False)
		goal.user = request.user
		tags = extract_hash_tags(request.POST.get('status-tags'))
		goal.save()
		for tag in tags:
			tag.save()
			tag.goal_set.add(goal)
			tag.save()

		return goal

	return ajax_form_view(request, GoalForm, success, "goals/form.html")


@login_required
def edit(request, goal_pk):
	goal = get_object_or_404(Goal, pk=goal_pk)
	if goal.user != request.user:
		raise PermissionDenied

	def success(form):
		goal = form.save(commit=False)
		goal.save()

		return goal

	return ajax_form_view(request, GoalForm, success, "goals/form.html", instance=goal)


@login_required
def delete(request, goal_pk):
	goal = get_object_or_404(Goal, pk=goal_pk)
	if goal.user != request.user:
		raise PermissionDenied

	goal.delete()

	return json_view()


@login_required
def add_comment(request, goal_pk):
	goal = get_object_or_404(Goal, pk=goal_pk)

	def success(form):
		goalcomment = form.save(commit=False)
		goalcomment.goal = goal
		goalcomment.user = request.user
		goalcomment.save()

		if goalcomment.user != goal.user:
			send_notification(
				goal.user,
				"%s %s commented on your goal \"%s\"." % (request.user.first_name, request.user.last_name, goal.title),
				"#goal/" + str(goal.pk) + "/view")

		return goalcomment

	return ajax_form_view(request, GoalCommentForm, success, "goals/comment_form.html",
						  template_variables={"goal": goal})


@login_required
def relist(request, goal_pk):
	relist_goal = get_object_or_404(Goal, pk=goal_pk)

	if request.method != "POST":
		new_goal = Goal(
			image=relist_goal.image,
			title=relist_goal.title,
			description=relist_goal.description,
		)

	else:
		new_goal = None

	def success(form):
		goal = form.save(commit=False)
		goal.user = request.user
		goal.save()

		GoalRelist(user=request.user, goal=relist_goal).save()

		return relist_goal.goalrelist_set.count()

	return ajax_form_view(request, GoalForm, success, "goals/form.html", instance=new_goal,
						  template_variables={"relist_goal": relist_goal})


@login_required
def like(request, goal_pk):
	goal = get_object_or_404(Goal, pk=goal_pk)

	try:
		goallike = GoalLike.objects.get(user=request.user, goal=goal)
		goallike.delete()
	except GoalLike.DoesNotExist:
		GoalLike(user=request.user, goal=goal).save()

	return json_view(goal.goallike_set.count())


@login_required
def done(request, goal_pk):
	goal = get_object_or_404(Goal, pk=goal_pk)
	if goal.user != request.user:
		raise PermissionDenied

	if request.method == "POST":
		form = DoneGoalForm(request.POST, request.FILES)
		if form.is_valid():
			cleaned_data = form.clean()

			if cleaned_data['image']:
				GoalImage(image=cleaned_data['image'], goal=goal).save()

			if cleaned_data['description']:
				goal.description = cleaned_data['description']

			goal.is_done = True
			goal.save()

		return redirect("/users/profile/") # users.views.profile

	return ajax_form_view(request,
						  DoneGoalForm,
						  None,
						  "goals/done.html",
						  template_variables={"goal": goal},
						  initial={"description": goal.description})


@login_required
def lifelist(request, user_pk):
	user = get_object_or_404(User, pk=user_pk)
	goals = Goal.objects.filter(user=user).order_by("created").all()

	return json_view(data=goals)


def done_goals(request, user_pk=None):
	if user_pk:
		user = get_object_or_404(User, pk=user_pk)
		done_goals = Goal.objects.filter(user=user, is_done=True).order_by("-created")
	else:
		done_goals = Goal.objects.filter(is_done=True).order_by("-created")[:20]

	return json_view(data=done_goals)


@login_required
def following_done_goals(request, user_pk):
	user = get_object_or_404(User, pk=user_pk)
	following_users = [x.target for x in request.user.following.all()]
	done_goals = Goal.objects.filter(user__in=following_users, is_done=True).order_by("-created")

	return json_view(data=done_goals)


@login_required
def search_by_tag(request, tag):
	return render(request, "goals/search_by_tag.html", {
		"tag": tag
	})

@login_required
def hashroll(request):
	top_tags = calculate_top_tags()
	tag = top_tags[randrange(0, len(top_tags))]
	return render(request, "goals/search_by_tag.html", {
		"tag": quote(tag)
	})


@login_required
def tag_form(request):
	def success(form):
		return form.cleaned_data.get("tag")

	return ajax_form_view(request, GoalTagForm, success, "goals/tag_form.html")

@login_required
def report(request, id):
	goal = get_object_or_404(Goal, id)
	goal.reports += 1
	if goal.reports <= 1:
		pass # send email

	return json_view(data=Goal.objects.filter(id=id))

def calculate_top_tags():
	tmp = [x.split(",") for x in Goal.objects.values_list("tags", flat=True)]

	occurrence = defaultdict(int)
	for x in tmp:
		for tag in [y.strip() for y in x]:
			if tag:
				occurrence[tag] += 1

	top_tags = [x[0] for x in sorted(occurrence.iteritems(), key=operator.itemgetter(1), reverse=True)[:settings.TOP_TAGS_COUNT]]
	return  top_tags

@login_required
def top_tags(request):
	top_tags = calculate_top_tags()
	return json_view(data=top_tags)


def view(request, goal_pk):
	goal = Goal.objects.get(pk=goal_pk)

	return render(request, "goals/view.html", {
		"goal": goal
	})
