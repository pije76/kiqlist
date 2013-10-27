"""
Django settings for kiqlist project.
"""

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#sys.path.insert(0, os.path.join(PROJECT_ROOT, 'kiqlist'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	("Jerome Leclanche", "jerome.leclanche+kiqlist@gmail.com"),
)

ALLOWED_HOSTS = ['*']

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/London"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	#os.path.join(PROJECT_ROOT, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
	# "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "sb1b31rf@og@q7oxv)sfnaxkb%ygrmn4%ah6^g4_jp5bs@4-rj"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	# Database templates have priority
	# "dbtemplates.loader.Loader",
	"django.template.loaders.filesystem.Loader",
	"django.template.loaders.app_directories.Loader",
	# "django.template.loaders.eggs.Loader",
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
	"social_auth.context_processors.social_auth_by_type_backends",
	"kiqlist.utils.functions.profile_processor"
)

MIDDLEWARE_CLASSES = (
	"django.middleware.common.CommonMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	# "django.middleware.locale.LocaleMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
)

ROOT_URLCONF = "kiqlist.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "kiqlist.wsgi.application"

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.flatpages",
	"django.contrib.humanize",
	"django.contrib.messages",
	"django.contrib.sites",
	"django.contrib.sessions",
	"django.contrib.staticfiles",
	"django.contrib.admin",
	"django.contrib.admindocs",

	"articles",
	"sorl.thumbnail",
	"social_auth",
	"south",
	"gunicorn",

	"kiqlist.goals",
	"kiqlist.notifications",
	"kiqlist.private_messages",
	"kiqlist.statuses",
	"kiqlist.users",
	"kiqlist.wiki_images",
	"kiqlist.hash_tags"
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"filters": {
		"require_debug_false": {
			"()": "django.utils.log.RequireDebugFalse"
		}
	},
	"formatters": {
		"verbose": {
			"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
		},
	},
	"handlers": {
		"console": {
			"level": "DEBUG",
			"class": "logging.StreamHandler",
			"formatter": "verbose"
		},
		"mail_admins": {
			"level": "ERROR",
			"filters": ["require_debug_false"],
			"class": "django.utils.log.AdminEmailHandler"
		}
	},
	"loggers": {
		"django.request": {
			"handlers": ["mail_admins"],
			"level": "ERROR",
			"propagate": True,
		},
	}
}

LOGIN_REDIRECT_URL = "/users/profile/"
LOGIN_URL = "/#login"
LOGOUT_URL = "/users/logout/"

AUTHENTICATION_BACKENDS = (
	"django.contrib.auth.backends.ModelBackend",
	"social_auth.backends.twitter.TwitterBackend",
	"social_auth.backends.facebook.FacebookBackend",
	"social_auth.backends.OpenIDBackend"
)

STATUSES_ON_PAGE_LIMIT = 5

WIKI_IMAGES_LIST_URL = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images"
WIKI_IMAGE_INFO_URL = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=imageinfo&iiprop=url&iiurlwidth=80&iiurlheight=80"
WIKI_IMAGES_EXT = [".png", ".jpg", ".jpeg"]
WIKI_IMAGES_LIMIT = 3

TOP_TAGS_COUNT = 5

NOTIFICATIONS_DAYS_CUTOFF = 7


def import_settings(module):
	"""
	Imports ``settings`` as a settings file, and:
	 - Sets any currently unset setting
	 - Merges any dictionary setting with the one currently set
	 - Extends any currently set tuple or list setting
	 - Replaces any other setting
	"""
	settings = __import__(module)
	if "." in module:
		for pkg in module.split(".")[1:]:
			settings = getattr(settings, pkg)

	for var in dir(settings):
		if not var.isupper() or var.startswith("_"):
			continue

		G = globals()
		setting = getattr(settings, var)

		if var not in G:
			G[var] = setting
		elif isinstance(setting, dict):
			G[var] = G[var].merge(setting)
		elif isinstance(setting, list) or isinstance(setting, tuple):
			G[var] += setting
		else:
			G[var] = setting

try:
	import_settings("kiqlist.live_settings")
except ImportError:
	pass
