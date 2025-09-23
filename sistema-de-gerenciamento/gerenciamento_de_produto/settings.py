from pathlib import Path
from django.contrib.messages import constants as message
import os 
import dj_database_url
import pymysql
pymysql.install_as_MySQLdb()

import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"









BASE_DIR = Path(__file__).resolve().parent.parent
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
]
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'SUA_CLIENT_ID'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SUA_CLIENT_SECRET'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4&a1%t^a0@(um_wzh^8vb5bt5$svuugo-#4$l8+z_ad1-hk*oe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'produtos',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
    'social_django',
    'cloudinary',  # novo
    'cloudinary_storage',  # novo

]
SITE_ID = 1

# settings.py
AUTH_USER_MODEL = 'produtos.Usuario'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'gerenciamento_de_produto.urls'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'gerenciamento_de_produto.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases







DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        default='mysql://cardapio:20232024@localhost:3306/gerenciamento_de_produto'
    )
}





'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gerenciamento_de_produto',
        'USER': 'cardapio',
        'PASSWORD': '20232024',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
'''



'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sdfsdf',
        'USER': 'ifmais',
        'PASSWORD': '1fp1',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS' : {
            'client_encoding': 'UTF8',
        },
        'CHARSET' : 'UTF8',
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/





STATIC_URL = 'static/'


    
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'WhiteNoise.storage.CompressedManifestStaticFilesStorage'    
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'produto_list'
LOGOUT_REDIRECT_URL = 'login'

AUTH_USER_MODEL = 'produtos.Usuario'


MESSAGE_TAGS = {
    message.DEBUG: 'debug',
    message.INFO: 'info',
    message.SUCCESS: 'success',
    message.WARNING: 'warning',
    message.ERROR: 'danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}