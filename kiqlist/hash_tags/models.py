from itertools import chain
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from kiqlist.goals.models import Goal
from kiqlist.statuses.models import Status


class HashTag(models.Model):
	title = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.title

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.title == other.title


def extract_hash_tags(tags_string):
	content_tags_titles = set(part[1:] for part in tags_string.split() if part.startswith('#'))
	existing_tags = HashTag.objects.all()
	ret = set()
	for nht in content_tags_titles:
		et = existing_tags.filter(title=nht)
		if et:
			ret.add(et.get())
		else:
			ret.add(HashTag(title=nht))
	return ret



def delete_hash_tag_orphans():
	tags_by_goals = Goal.tags.through.objects.values_list('hashtag', flat=True).distinct()
	tags_by_status = Status.tags.through.objects.values_list('hashtag', flat=True).distinct()
	tags_in_use = list(chain(tags_by_goals, tags_by_status))
	orphans = HashTag.objects.exclude(pk__in=tags_in_use)
	orphans.delete()


@receiver(post_delete, sender=Status)
def status_post_delete(sender, **kwargs):
	delete_hash_tag_orphans()


@receiver(post_delete, sender=Goal)
def goal_post_delete(sender, **kwargs):
	delete_hash_tag_orphans()