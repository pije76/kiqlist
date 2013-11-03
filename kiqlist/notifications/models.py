from datetime import datetime, timedelta
from time import mktime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc


class Notification(models.Model):
	content = models.TextField()
	url = models.URLField(blank=True, null=True)
	user = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	is_unread = models.BooleanField(default=True)
	is_new = models.BooleanField(default=True)

	def display_dict(self):
		cssClass = ''
		if self.is_new:
			cssClass = 'new-notification'
		if self.is_unread:
			if cssClass:
				cssClass += ' '
			cssClass += 'unread-notification'

		return {
			"pk": self.pk,
			"fields": {
				"content": self.content,
				"url": self.url,
				"created": mktime(self.created.timetuple()),
				"isUnread": self.is_unread,
				"isNew": self.is_new,
				"cssClass": cssClass,
				"age": self.get_age()
			}
		}

	def get_age(self):
		time_passed = datetime.now().replace(tzinfo=utc) - self.created
		ret = '%d '
		if time_passed < timedelta(seconds=60):
			amount = time_passed.seconds
			ret += 'second' if amount == 1 else 'seconds'
		elif time_passed < timedelta(seconds=3600):
			amount = time_passed.seconds / 60
			ret += 'minute' if amount == 1 else 'minutes'
		elif time_passed < timedelta(days=1):
			amount = time_passed.seconds / 3600
			ret += 'hour' if amount == 1 else 'hours'
		else:
			amount = time_passed.days
			ret += 'day' if amount == 1 else 'days'
		return (ret + ' ago') % amount