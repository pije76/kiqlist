from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("",
	url(r"^$", "kiqlist.views.home", name="home"),
	url(r"^about/contact/", include("contact_form.urls")),
	url(r"^blog/", include("articles.urls")),
	url(r"^dashboard/$", "kiqlist.views.dashboard", name="dashboard"),
	url(r"^users/", include("kiqlist.users.urls")),
	url(r"^tags/", include("kiqlist.hash_tags.urls")),
	url(r"^statuses/", include("kiqlist.statuses.urls")),
	url(r"^goals/", include("kiqlist.goals.urls")),
	url(r"^pm/", include("kiqlist.private_messages.urls")),
	url(r"^notifications/", include("kiqlist.notifications.urls")),
	url(r"^wiki/images/", include("kiqlist.wiki_images.urls")),
	url(r"^js_templates/(?P<name>\w+)\.html$", "kiqlist.utils.views.serve_js_templates"),
	url(r"^accounts/", include("social_auth.urls")),

	url(r"^content/done/(?P<user_pk>\d+)/$", "kiqlist.views.content_done"),
	url(r"^content/done/$", "kiqlist.views.content_done"),
	url(r"^content/following/$", "kiqlist.views.following"),

	# Site administration
	url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
	url(r"^admin/", include(admin.site.urls)),

	# Media
	url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
)
