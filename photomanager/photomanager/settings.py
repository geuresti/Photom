from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jf03p45+joxwgq@6^ms)uo-y_@_!*#6z#@-@k7fm%%y!zi7k)a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'photom.apps.PhotomConfig',
    'phonenumber_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photomanager.urls'

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

WSGI_APPLICATION = 'photomanager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

"""
# PA Hosting *
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "photomadmin",
        "PASSWORD": "s^k4Fv05@",
        "HOST": "gioeuresti-3742.postgres.pythonanywhere-services.com",
        "PORT": "13742",
    }
}
"""

# Local Postgresql
#        "PORT": "5432",

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "photom",
        "USER": "postgres",
        "PASSWORD": "k$a#g27H",
    }
}

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'spi.photo.manager@gmail.com'
EMAIL_HOST_PASSWORD = 'ciyx dpma matv tmjt'
"""

LANGUAGE_CODE = 'en-us'

PHONENUMBER_DEFAULT_REGION = "US"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/photom/login/'

LOGIN_REDIRECT_URL = '/photom/'

LOGOUT_REDIRECT_URL = '/photom/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'