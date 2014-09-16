"""
Django settings for rbmo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH   = os.path.join(BASE_DIR, 'static')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*d#x#)e90lxef!jl^nk3#^rq2-#dksb91cuqtra%p2t4++tpc8'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

TEMPLATE_DEBUG = True

SESSION_EXPIRE_AT_BROWSER_CLOSE=True

ADMINS = ('Jofel Bayron', 'bayron.jofel@gmail.com')

ALLOWED_HOSTS = ['byrenx.pythonanywhere.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth.hashers',
    'django.contrib.humanize',
    'rbmo',
    'admin',
    'fund',
    'wfp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rbmo.urls'

WSGI_APPLICATION = 'rbmo.wsgi.application'

TEMPLATE_DIRS = (TEMPLATE_PATH.replace('\\','/'),)
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#mysql settings 
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rbmo',                      
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',     
    }
}
'''

#pythonanywhere settings

DATABASES = {
    'default': {        
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'byrenx$rbmo',                      
        # The following settings are not used with sqlite3:
        'USER': 'byrenx',

        'PASSWORD': 'byREnX++0789',
        'HOST': 'mysql.server',                      
        'PORT': '',                   
    }
}


#postgre sql settings
'''
DATABASES = {
    'default': {
        
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'rbmo2',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        #'PASSWORD': 'DEVELOPERS',
        'PASSWORD': 'byrenx',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}
'''

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = ( STATIC_PATH.replace('\\','/'),
   #'E:/Projects/pis_system/templates/static',
   # '/home/rasmer/PycharmProjects/pis_system/templates/static',
)
