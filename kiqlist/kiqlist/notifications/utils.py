from .models import Notification


def send_notification(user, content, url):
	Notification(user=user, content=content, url=url).save()
