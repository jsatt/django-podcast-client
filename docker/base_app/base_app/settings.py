import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'keepitsecret'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'kombu.transport.django',

    'podcast_client',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'base_app.urls'

WSGI_APPLICATION = 'base_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/database.db',
    },
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = '/downloads'
PODCAST_DIRECTORY = '.'

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

TRANSMISSION = {}
transmission_address = os.environ.get('TRANSMISSION_HOST')
if transmission_address:
    TRANSMISSION['address'] = transmission_address
transmission_port = os.environ.get('TRANSMISSION_PORT')
if transmission_port:
    TRANSMISSION['port'] = transmission_port
transmission_user = os.environ.get('TRANSMISSION_USER')
if transmission_user:
    TRANSMISSION['user'] = transmission_user
transmission_password = os.environ.get('TRANSMISSION_PASSWORD')
if transmission_password:
    TRANSMISSION['password'] = transmission_password
