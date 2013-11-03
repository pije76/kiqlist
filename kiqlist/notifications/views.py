from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.timezone import utc
from kiqlist.settings import NOTIFICATIONS_DAYS_CUTOFF
from kiqlist.utils.views import json_view
from .models import Notification


@login_required
def new(request):
	delete(request)
	notifications = Notification.objects.filter(user=request.user).order_by('-created')[:10]
	new_notifications = Notification.objects.filter(user=request.user, is_new=True);
	count_new = len(new_notifications)

	response = {
		"data": {
			"notifications": [n.display_dict() for n in notifications],
			"count_new": count_new
		},
		"error_code": 0
	}

	return HttpResponse(json.dumps(response), mimetype="application/json")

@login_required
def mark_as_old(request):
	pks = request.GET.get('pks').split(',')
	if len(pks) > 0 and pks[0]:
		Notification.objects.filter(user=request.user, pk__in=pks).update(is_new=False)

	return json_view()


@login_required
def all(request):
	notifications = Notification.objects.filter(user=request.user).order_by('-created')
	return json_view(notifications);

@login_required
def read(request, notification_pk):
	try:
		notification = Notification.objects.get(pk = notification_pk)
	except Notification.ObjectNotFound:
		return json_view(error=(1, "Wrong request."))

	notification.is_unread = False
	notification.save()

	return json_view()


@login_required
def delete(request):
	try:
		date_cutoff_delta = timedelta(days = NOTIFICATIONS_DAYS_CUTOFF)
		date_cutoff = datetime.now().replace(tzinfo=utc) - date_cutoff_delta
		notifications = Notification.objects.filter(
			user = request.user,
			created__lt = date_cutoff
		)
	except Notification.ObjectNotFound:
		return json_view(error=(1, "Wrong request."))

	notifications.delete()

	return json_view()
