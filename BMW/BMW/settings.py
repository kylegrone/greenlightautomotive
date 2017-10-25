"""
Testing Django settings for BMW project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1+38ura3$y8k7xskj1o0+h+%ql5=3s3c15cu5uz@w=9l$%7ich'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
'django.contrib.sites',
    'dealership',
    'customer',
    'flagging',
    'livechat',
	'mobilecheckin',
#'subdomains'
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                 'django.core.context_processors.request'
            ],
        },
    },
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
  #  'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'customer.middelware.TimeZoneMiddleware',
)

ROOT_URLCONF = 'BMW.urls'

WSGI_APPLICATION = 'BMW.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databas

DATABASES = {

    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'pr01mydb01',
         'USER': 'rootdbpr01',
         'PASSWORD': 'Telenor-345',
         'HOST': 'mysqldpr01.cunpgfdq8hpq.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
         'PORT': '3306',
      }
 } 
'''DATABASES = {
      
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BMW',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
     }
}'''

 
DATABASES = {
       
   'default': {
         'NAME': 'bmw',
        'ENGINE': 'mysql.connector.django',
        'USER': 'root',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'PASSWORD': '',
        'OPTIONS': {
          'autocommit': True,
        },
     }
}
  

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
#)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = 'sender.bmw.projec@gmail.com'
#EMAIL_HOST_PASSWORD = 'BMW12345'
#EMAIL_PORT = 587
EMAIL_PORT = 25
#CENTRIFUGE_URL ="https://bmw-elosophy.herokuapp.com/connection";
#CENTRIFUGE_SECRET = "demo";
CENTRIFUGE_URL ="https://bmw-elosophy.herokuapp.com/connection";#used for javascript librarires
CENTRIFUGE_API_URL ="https://bmw-elosophy.herokuapp.com/";
CENTRIFUGE_SECRET = "demo";
CENTRIFUGE_KEY = "bmw-elosophy"
MAP_KEY = "AIzaSyArTVoMmtYJ87Eb6FIveZ-IqX1WJ2HPf8Y"
APPROVAL_REQUIRED_FLAG_ID = 43
CAR_WASH_FLAG_ID = 46
UBER_ID = 46
# SITE_MAIN_URL ="http://202.165.228.25:8080"
SITE_MAIN_URL ="http://greenlightautomotive.com"
SITE_MAIN_URL ="http://greenlightautomotive.com"
BMW_MAKE_CODE = "u"


PAYPAL_CLIENT_ID = "ARfL_wcV0YdvLyobp_ic4vA-qWqKKLCku7s7Ck9VK7oGSCm0hO6vPW3jk9OIAuevLG0au6a8m8uqVNqi"
PAYPAL_SECRET = "EJXORrojmCIvcv0yqru4qgZmJ_cI4Gz8khki0eJyQCrZN5XdUmMM_N-owz1bwNL0OkWH88MXofD_uf8M"
PAYPAL_MODE = "sandbox"
SITE_ID = 1

"""
ROOT_URLCONF = 'customer.urls'
# 
SUBDOMAIN_URLCONFS = {
    None: 'customer.urls',
    'customer': 'customer.urls',
    'dealership': 'dealership.urls',
    'mobilecheckin': 'mobilecheckin.urls',
    'flagging': 'flagging.urls',
}

"""

TWILIO_SID="AC6168bee50e34f6fe6f1b021356bde3cc"
TWILIO_AUT="4754452df8b3386e34f60751f7682f9b"
TWILIO_DEFAULT="+13312156289"
DEFAULT_EMAIL_FROM = "admin@greenlighautomotive.com"
