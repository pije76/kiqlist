from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.private_messages.views",
	url(r"index/$", "index"),
	url(r"conversation/(?P<interlocutor_pk>\d+)/$", "conversation"),
	url(r"add_private_message/$", "add_private_message"),
	url(r"start_conversation/$", "start_conversation")
)
