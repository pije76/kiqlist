from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.statuses.views",
	url(r"add/$", "add"),
	url(r"delete/(?P<status_pk>\d+)/$", "delete"),
	url(r"list/following/$", "following_list"),
	url(r"list/user/(?P<user_pk>\d+)/$", "user_list"),
	url(r"reply/(?P<status_pk>\d+)/$", "reply"),
)
