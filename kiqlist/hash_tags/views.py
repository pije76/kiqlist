from itertools import chain
from operator import attrgetter
from random import randrange
from urllib import quote
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.shortcuts import render

from kiqlist.goals.models import Goal
from kiqlist.hash_tags.forms import HashTagForm
from kiqlist.hash_tags.models import HashTag
from kiqlist.statuses.models import Status
from kiqlist.utils.views import json_view, ajax_form_view

@login_required
def search(request, tag):
	goals = Goal.objects.filter(tags__title__exact=tag)
	statuses = Status.objects.filter(tags__title__exact=tag)
	data = sorted(
		chain(goals, statuses),
		key=attrgetter('created'),
		reverse=True
	)
	return data


@login_required
def tag_form(request):
	def success(form):
		return form.cleaned_data.get("tag")

	return ajax_form_view(request, HashTagForm, success, "hash_tags/tag_form.html")

@login_required
def json_search_by_tag(request, tag):
	return json_view(data=search(request, tag))


@login_required
def search_by_tag(request, tag):
	return render(request, 'hash_tags/search_by_tag.html', {
		"tag": quote(tag)
	})


@login_required
def hashroll(request):
	tags_count = HashTag.objects.all() \
		.annotate(count_goal=Count('goal')) \
		.annotate(count_status=Count('status'))
	top_tags = sorted(
		tags_count,
		key=lambda row: row.count_goal + row.count_status,
		reverse=True
	)[:settings.TOP_TAGS_COUNT]
	chosen_tag = top_tags[randrange(0, len(top_tags))]
	return search_by_tag(request, quote(chosen_tag.title))