from django.conf.urls import patterns, url

urlpatterns = patterns("kiqlist.hash_tags.views",
	url(r"json/search/(?P<tag>\S+)", "json_search_by_tag"),
	url(r"search/(?P<tag>\S+)", "search_by_tag"),
	url(r"hashroll/$", "hashroll"),
	url(r"tag_form/$", "tag_form"),
)