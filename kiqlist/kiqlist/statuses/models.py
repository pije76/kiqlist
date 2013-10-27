from time import mktime

from django.db import models


class Status(models.Model):
	content = models.CharField(max_length=140)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	user = models.ForeignKey("auth.User")
	tags = models.ManyToManyField("hash_tags.HashTag")

	def display_dict(self):
		return {
			"pk": self.pk,
			"type": "status",
			"fields": {
				"content": self.content,
				"created": self.created.strftime("%H:%M, %d %B %Y"),
				"created-raw": mktime(self.created.timetuple()),
				"user": {
					"pk": self.user.pk,
					"first_name": self.user.first_name,
					"last_name": self.user.last_name
				},
				"tags": [x.title for x in self.tags.all().order_by('title')] if self.tags else None
			}
		}