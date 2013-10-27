from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.notifications.views",
	url(r"new/$", "new"),
	url(r"delete/$", "delete"),
	url(r"read/(?P<notification_pk>\d+)/$", "read"),
	url(r"all/$", "all"),
	url(r"mark_old$", "mark_as_old")
)
