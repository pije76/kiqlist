from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.goals.views",
	url(r"lifelist/(?P<user_pk>\d+)/$", "lifelist"),
	url(r"add/$", "add"),
	url(r"edit/(?P<goal_pk>\d+)/$", "edit"),
	url(r"delete/(?P<goal_pk>\d+)/$", "delete"),
	url(r"done/(?P<goal_pk>\d+)/$", "done"),
	url(r"add_comment/(?P<goal_pk>\d+)/$", "add_comment"),
	url(r"relist/(?P<goal_pk>\d+)/$", "relist"),
	url(r"report/(?P<id>\d+)/$", "report", name="goal_report"),
	url(r"like/(?P<goal_pk>\d+)/$", "like"),
	url(r"done/list/$", "done_goals"),
	url(r"done/list/(?P<user_pk>\d+)/$", "done_goals"),
	url(r"done/list/(?P<user_pk>\d+)/following/$", "following_done_goals"),
	url(r"tag/(?P<tag>\S+)/$", "search_by_tag"),
	url(r"tag_form/$", "tag_form"),
	url(r"top_tags/$", "top_tags"),
	url(r"view/(?P<goal_pk>\d+)/$", "view"),
	url(r"hashroll$", "hashroll")
)
