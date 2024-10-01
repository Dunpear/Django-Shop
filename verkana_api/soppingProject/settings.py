from datetime import timedelta
from pathlib import Path
from os import path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pysih=(_&rhs0p1=v-7)=8%l$kp!t99yt&zgwar5qah+9=p6nb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',  # Add your frontend domain here
)

# Application definition

INSTALLED_APPS = [
    'drf_spectacular',
    'rest_framework',
    'django_jalali',
    'rest_framework_simplejwt',
    'ckeditor',
    'ckeditor_uploader',
    'colorfield',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'apps.account.apps.AccountConfig',
    'apps.slider.apps.SliderConfig',
    'apps.banner.apps.BannerConfig',
    'apps.blog.apps.BlogConfig',
    'apps.main.apps.MainConfig',
    'apps.product.apps.ProductConfig',
    'apps.comment.apps.CommentConfig',
    'apps.invoice.apps.InvoiceConfig',
    'apps.paymentgateway.apps.PaymentgatewayConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'soppingProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'soppingProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'verkana',
        'USER': 'root',
        'PASSWORD': '0122',
        'OPTIONS': {
            'autocommit': True
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CKEDITOR_UPLOAD_PATH = 'ckeditor/upload_files/'
CKEDITOR_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Link', 'Unlink', 'Image'],
        ]
    },
    'special': {
        'toolbar': 'Special',
        'height': 200,
        'toolbar': 'full',
        'toolbar_Special': [
            ['Bold', 'Italic', 'Underline', 'Link', 'Unlink', 'Image'],
            ['CodeSnippet'],

        ], 'extraPlugins': ','.join(['codesnippet', 'clipboard'])
    },
    'special_an': {
        'toolbar': 'Special',
        'height': 200,
        'toolbar_Special': [
            ['Bold'],
            ['CodeSnippet'],
        ], 'extraPlugins': ','.join(['codesnippet', 'clipboard'])
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (path.join(BASE_DIR, 'static/'),)

MEDIA_URL = 'media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media/')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.CustomerUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'Verkana Api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # OTHER SETTINGS
}
