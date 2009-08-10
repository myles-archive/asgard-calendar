DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/asgard-calendar-devel.db'
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.comments',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.sites',
	'django.contrib.sitemaps',
	'django.contrib.humanize',
	
	'tagging',
	
	'asgard.locations',
	'asgard.calendars',
]
ROOT_URLCONF = 'asgard.calendars.testurls'