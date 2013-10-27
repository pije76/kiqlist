from django.db import models
from django.contrib.auth.models import User


class PrivateMessage(models.Model):
	from_user = models.ForeignKey(User, related_name="outbox")
	to_user = models.ForeignKey(User, related_name="inbox")
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True, editable=False)
