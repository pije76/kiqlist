from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class ActivationKey(models.Model):
	user = models.ForeignKey(User)
	key = models.CharField(max_length=100)

	def __unicode__(self):
		return "Activation key for %s" % (self.user)


class Profile(models.Model):
	photo = models.ImageField(upload_to="user_photos", null=True, blank=True)
	about = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.user.__unicode__()

	def get_followers_count(self):
		return Follow.objects.filter(target=self.user).count()


class Follow(models.Model):
	user = models.ForeignKey(User, related_name="following")
	target = models.ForeignKey(User, related_name="followers")
	created = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	user = kwargs["instance"]

	if not Profile.objects.filter(user=user).exists():
		Profile(user=user).save()
