import sys
from misago.settings_base import *
import dj_database_url
import os

# Allow debug?
DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Board address
BOARD_ADDRESS = os.environ.get('BOARD_ADDRESS')

# Installed applications
INSTALLED_APPS = (
    # Applications that have no dependencies first!
    'south',  # Database schema building and updating
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_jinja',  # Jinja2 integration
    'django_jinja.contrib._humanize',  # Some Django filters
    'floppyforms',  # Better forms
    'mptt',  # Modified Pre-order Tree Transversal - allows us to nest forums
    'haystack',  # Search engines bridge
    'debug_toolbar',  # Debug toolbar'
    'misago',  # Misago Forum App
    'app',
    'votes',
    'party',
    'blog',
    'storages'
)

# Admin control panel path
# Leave this setting empty or remove it to turn admin panel off.
# Misago always asserts that it has correct admin path and fixes it
# if neccessary. This means "/admincp////" becomes "admincp/" and
# "administration" becomes "administration/"
ADMIN_PATH = 'forum/admincp'

# System admins
# Enter every god admin using following pattern:
# ('John', 'john@example.com'),
# Note trailing separator!
ADMINS = (('Admin', os.environ.get('ADMIN_EMAIL')),)

# Secret key is used by Django and Misago in hashes generation
# YOU MUST REPLACE IT with random combination of characters
# NEVER EVER SHARE THIS KEY WITH ANYBODY!
# Make it messed up and long, this is example of good secret key:
# yaobeifl1a6hf&3)^uc#^vlu1ud7xp^+*c5zoq*tf)fvs#*o$#
SECRET_KEY = "os.environ.get('SECRET_KEY')"

# Database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cache engine
# Misago is EXTREMELY data hungry
# If you don't set any cache, it will BRUTALISE your database and memory
# In production ALWAYS use cache
# For reference read following document:
# https://docs.djangoproject.com/en/dev/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Search engine
# Misago relies on 3rd party search engines to index and search your forum content
# Read following for information on configurating search:
# http://django-haystack.readthedocs.org/en/latest/tutorial.html#modify-your-settings-py
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',  # Misago uses Whoosh by default
        'PATH': 'searchindex',
    },
}

# Cookies configuration
COOKIES_DOMAIN = ''  # E.g. a cookie domain for "www.mysite.com" or "forum.mysite.com" is ".mysite.com"
COOKIES_PATH = '/'
COOKIES_PREFIX = 'ap3nAsA1un0S'  # Allows you to avoid cookies collisions with other applications.
COOKIES_SECURE = False  # Set this to true if, AND ONLY IF, you are using SSL on your forum.

# Sessions configuration
SESSION_LIFETIME = 3600  # Number of seconds since last request after which session is marked as expired.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

# Django Storages settings

# AWS Keys
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# S3 Bucket
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# AWS Domain
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# File Storage systsm for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Absolute filesystem path to the directory that will hold publicly available media uploaded by users.
# Always use forward slashes, even on Windows.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_ROOT_S3 = '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

# Absolute filesystem path to the directory that will hold post attachments.
# Always use forward slashes, even on Windows.
# Example: "/home/media/media.lawrence.com/attachments/"
ATTACHMENTS_ROOT = '/attachments/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# Always use forward slashes, even on Windows.
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# os.path.join(BASE_DIR, 'staticfiles')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# Always use forward slashes, even on Windows.
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# Using AWS for this. Previous was Local, '/static/'
STATIC_URL = '/static/'

# try to use S3 to hold storages.
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# whitenoise.django.GzipManifestStaticFilesStorage

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Make sure directory containing avatars is located under first directory on list
    os.path.join(BASE_DIR, 'misago/static'),
    os.path.join(BASE_DIR, 'app/static'),
)

# E-mail host
EMAIL_HOST = 'smtp.gmail.com'

# E-mail port
EMAIL_PORT = 587

# E-mail host user
EMAIL_HOST_USER = os.environ.get('EMAIL_ACCOUNT')

# E-mail host password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Use TLS encryption
EMAIL_USE_TLS = True

# This address is used in "from" field of emails sent by site
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_ACCOUNT')

# Screamer Configuration
# Screamer is special feature that sends email to users listed under ADMINS when application
# erros. First setting is origin of error emails, while second is message title prefix that
# makes messages easier to spot in your inbox
SERVER_EMAIL = os.environ.get('EMAIL_ACCOUNT')
EMAIL_SUBJECT_PREFIX = '[ApenasAlunos Screamer]'

# Catch-all e-mail address
# If DEBUG_MODE is on, all emails will be sent to this address instead of real recipient.
CATCH_ALL_EMAIL_ADDRESS = ''

# Directories with templates
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'misago/templates'),
    os.path.join(BASE_DIR, 'app/templates'),
)

# List of installed themes
INSTALLED_THEMES = (
    'cranefly', # Default style always first
    'admin', # Admin theme always last
)

# Enable mobile subdomain for mobile stuff
MOBILE_SUBDOMAIN = ''

# Templates used by mobile version
MOBILE_TEMPLATES = ''

# Name of root urls configuration
ROOT_URLCONF = 'deployment.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deployment.wsgi.application'

# # Empty secret key if its known
# if SECRET_KEY == 'yaobeifl1a6hf&3)^uc#^vlu1ud7xp^+*c5zoq*tf)fvs#*o$#':
#     SECRET_KEY = ''

# Disable Jinja2 for django debug toolbar templates
if DEBUG:
    DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r"(?!debug_toolbar/).*"

# Override config if we are in tests
if 'test' in sys.argv:
    if not SECRET_KEY:
        SECRET_KEY = 'SECRET4TESTS'
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db4testing'}
    CACHES['default'] = {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    SKIP_SOUTH_TESTS = True
    MEDIA_URL = "http://media.domain.com/"
    HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',},}
