from time import mktime

from django.db import models
from sorl.thumbnail import get_thumbnail

from kiqlist.users.models import Profile


class Goal(models.Model):
	image = models.URLField(max_length=1000, blank=True)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	due_date = models.DateField(blank=True, null=True)
	tags = models.ManyToManyField("hash_tags.HashTag")
	user = models.ForeignKey("auth.User")
	created = models.DateTimeField(auto_now_add=True, editable=False)
	is_done = models.BooleanField(default=False)
	need_help = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	@classmethod
	def display_user_dict(cls, user):
		return {
			'pk' : user.pk,
			'first_name' : user.first_name,
			'last_name' : user.last_name
		}

	def display_dict(self):
		goal_images = []
		for image in self.goalimage_set.all():
			goal_images.append(get_thumbnail(image.image, "320", crop="center", quality=99))

		profile = Profile.objects.get(user=self.user)
		if profile.photo:
			user_photo_thumbnail = get_thumbnail(profile.photo, "40x40", crop="center", quality=99)
			user_photo_thumbnail_url = user_photo_thumbnail.url
		else:
			user_photo_thumbnail_url = None

		return {
			"pk": self.pk,
			"type": "goal",
			"fields": {
				"title": self.title,
				"description": self.description,
				"due_date": self.due_date.strftime("%d %B %Y") if self.due_date else None,
				"tags": [x.title for x in self.tags.all().order_by('title')] if self.tags else None,
				"created": self.created.strftime("%d %B %Y"),
				"created-raw": mktime(self.created.timetuple()),
				"is_done": self.is_done,
				"user": {
					"pk": self.user.pk,
					"first_name": self.user.first_name,
					"last_name": self.user.last_name,
					"profile": {
						"photo": user_photo_thumbnail_url
					}
				},
				"image": self.image,
				"images": [x.url for x in goal_images],
				"comments": [x.display_dict() for x in self.goalcomment_set.all()],
				"counters": {
					"like_users": [Goal.display_user_dict(x.user) for x in self.goallike_set.all()],
					"relist_users": [Goal.display_user_dict(x.user) for x in self.goalrelist_set.all()]
				},
				"need_help" : self.need_help
			}
		}


class GoalImage(models.Model):
	image = models.ImageField(upload_to="goal_images")
	goal = models.ForeignKey(Goal)
	reports = models.PositiveIntegerField(default=0)


class GoalComment(models.Model):
	content = models.TextField()
	user = models.ForeignKey("auth.User")
	goal = models.ForeignKey(Goal)
	created = models.DateTimeField(auto_now_add=True, editable=False)

	def display_dict(self):
		profile = Profile.objects.get(user=self.user)

		if profile.photo:
			user_photo_thumbnail = get_thumbnail(profile.photo, "40x40", crop="center", quality=99)
			user_photo_thumbnail_url = user_photo_thumbnail.url
		else:
			user_photo_thumbnail_url = None

		return {
			"pk": self.pk,
			"fields": {
				"content": self.content,
				"created": self.created.strftime("%H:%M, %d %B %Y"),
				"user": {
					"pk": self.user.pk,
					"first_name": self.user.first_name,
					"last_name": self.user.last_name,
					"photo": user_photo_thumbnail_url
				}
			}
		}


class GoalLike(models.Model):
	user = models.ForeignKey("auth.User")
	goal = models.ForeignKey(Goal)


class GoalRelist(models.Model):
	user = models.ForeignKey("auth.User")
	goal = models.ForeignKey(Goal)
