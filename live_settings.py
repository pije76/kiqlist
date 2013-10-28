DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
		"NAME": "kiqlist",                      # Or path to database file if using sqlite3.
		"USER": "postgres",                      # Not used with sqlite3.
		"PASSWORD": "postgres",                  # Not used with sqlite3.
		"HOST": "",                      # Set to empty string for localhost. Not used with sqlite3.
		"PORT": "5433",                      # Set to empty string for default. Not used with sqlite3.
	}
}

ADMINS = (
	("Jerome Leclanche", "jerome.leclanche+kiqlist@gmail.com"),
)
