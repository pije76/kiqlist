from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from kiqlist.hash_tags.models import extract_hash_tags
from kiqlist.utils.views import ajax_form_view, json_view
from .forms import StatusForm
from .models import Status


@login_required
def add(request):
	def success(form):
		status = form.save(commit=False)
		status.user = request.user
		tags = extract_hash_tags(request.POST.get('status-tags'))
		status.save()
		for tag in tags:
			tag.save()
			tag.status_set.add(status)
			tag.save()

		return status

	return ajax_form_view(request, StatusForm, success, "statuses/form.html")


@login_required
def delete(request, status_pk):
	status = get_object_or_404(Status, pk=status_pk)

	if status.user != request.user:
		return json_view(error=(1, "Permission denied."))

	status.delete()
	return json_view()


@login_required
def following_list(request):
	users = [x.target for x in request.user.following.all()]
	offset = int(request.GET.get("offset", 0))
	data = Status.objects.filter(user__in=users).order_by("-created")[offset:offset + settings.STATUSES_ON_PAGE_LIMIT]

	return json_view(data=data)


@login_required
def user_list(request, user_pk):
	user = get_object_or_404(User, pk=user_pk)
	offset = int(request.GET.get("offset", 0))
	data = Status.objects.filter(user=user).order_by("-created")[offset:offset + settings.STATUSES_ON_PAGE_LIMIT]

	return json_view(data=data)


@login_required
def reply(request, status_pk):
	reply_status = get_object_or_404(Status, pk=status_pk)

	if request.method != "POST":
		new_status = Status(content="@%s%s" % (reply_status.user.first_name, reply_status.user.last_name))
	else:
		new_status = None

	def success(form):
		status = form.save(commit=False)
		status.user = request.user
		status.save()

	return ajax_form_view(request, StatusForm, success, "statuses/form.html", instance=new_status, template_variables={"reply_status": reply_status})
