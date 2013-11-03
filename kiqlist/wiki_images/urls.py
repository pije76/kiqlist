from django.conf.urls import patterns, include, url


urlpatterns = patterns("kiqlist.wiki_images.views",
	url(r"list/$", "get_list"),
)
