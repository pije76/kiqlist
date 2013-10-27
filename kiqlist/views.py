from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from kiqlist.goals.models import Goal
from kiqlist.statuses.models import Status
from kiqlist.utils.views import json_view


def home(request):
	return render(request, "home.html", {})



def dashboard(request):
	return render(request, "dashboard.html", {})



def content_done(request, user_pk=None):
	if user_pk:
		user = get_object_or_404(User, pk=user_pk)
		done_goals = Goal.objects.filter(user=user, is_done=True)
		statuses = Status.objects.filter(user=user)
	else:
		done_goals = Goal.objects.filter(is_done=True)[:10]
		statuses = Status.objects.all()[:10]

	data = sorted(
		chain(done_goals, statuses),
		key=attrgetter('created'),
		reverse=True
	)

	return json_view(data=data)


def following(request):
	following_users = [x.target for x in request.user.following.all()]
	goals = Goal.objects.filter(user__in=following_users)
	statuses = Status.objects.filter(user__in=following_users)

	data = sorted(
		chain(goals, statuses),
		key=attrgetter('created'),
		reverse=True
	)

	return json_view(data=data)