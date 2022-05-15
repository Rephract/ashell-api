import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '!+bidy*q6zdpw(k5=aj_0e#uw_aw+t-zkt4@2v6z1$6v5a^7d-'
DEBUG = os.environ.get('DEBUG') == 'True'
ALLOWED_HOSTS = ['127.0.0.1', 'app.awareshell.com', 'stg-app.awareshell.com', 'localhost']


# Application definition

AUTH_USER_MODEL = 'account.User'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'account',
    'campaign',
    'core',
    'oauth2_provider'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',

]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '500/minute',
        'user': '1000/minute',

    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# SMTP
DEFAULT_FROM_EMAIL = "Awareshell Account Confirmation <%s>" % "account@awareshell.com"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_IGNORE_RESULT = True
CELERY_BROKER_URL = os.environ.get(
    'CELERY_URL', 'redis://:1qvSgjrAIRAHqD2ZqdV1Ojzxw@localhost:6379/1'
)
CELERYD_HIJACK_ROOT_LOGGER = False
REDIS_CHANNEL_URL = os.environ.get(
    'REDIS_CHANNEL_URL', 'redis://:1qvSgjrAIRAHqD2ZqdV1Ojzxw@localhost:6379/0'
)

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24 * 30
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": not DEBUG,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s:=> %(message)s", },
    },
    "handlers": {
        "log_docker": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["log_docker"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

AUTH_CLIENT_ID = os.environ.get('AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET = os.environ.get('AUTH_CLIENT_SECRET')
