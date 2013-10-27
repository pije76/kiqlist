from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.users.views",
	url(r"register/$", "register"),
	url(r"login/$", "login"),
	url(r"logout/$", "logout"),
	url(r"edit_profile/$", "edit_profile"),
	url(r"edit_password/$", "edit_password"),
	url(r"edit_profile_photo/$", "edit_profile_photo"),
	url(r"activate/(?P<key>\w+)/$", "activate"),
	url(r"profile/$", "profile"),
	url(r"profile/(?P<user_pk>\d+)/$", "profile"),
	url(r"friends/$", "friends"),
	url(r"unfollow/(?P<user_pk>\d+)/$", "unfollow"),
	url(r"follow/(?P<user_pk>\d+)/$", "follow"),
	url(r"settings/$", "settings"),
	url(r"activity/following/$", "following_activity")
)
