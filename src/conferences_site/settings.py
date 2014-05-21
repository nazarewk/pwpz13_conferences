import os

_ = lambda s: s

TEMPLATE_CONTEXT_PROCESSORS = []
MIDDLEWARE_CLASSES = []
TEMPLATE_DIRS = []

SITE_ID = 1
SITE_URL = ''
SITE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(SITE_DIR)

INTERNAL_IPS = ('127.0.0.1',)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'or9z37q6hj^)dk%$(w&@md-4vu#o&tjah=g%+nk@3hfl36r-4e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # CMS
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a modified pre-order traversal tree
    'menus',  # helper for model independent hierarchical website
    'sekizai',  # for javascript and css management
    'djangocms_admin_style',
    # for the admin skin. You **must** add 'djangocms_admin_style' in the list before 'django.contrib.admin'.
    'django.contrib.messages',  # to enable messages framework (see :ref:`Enable messages <enable-messages>`)
    'reversion',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'sekizai',
    'easy_thumbnails',
    'conferences',

    'django_extensions',
    'debug_toolbar',
    'session_security',
    'south',  # intelligent schema and data migrations
]

MIDDLEWARE_CLASSES += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conferences_site.urls'

WSGI_APPLICATION = 'conferences_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


# ##################################
# Locale/Internationalization   #
###################################
TIME_ZONE = 'Europe/Warsaw'

LANGUAGES = (
    ('pl', _(u'Polski')),
    ('en', _(u'Angielski')),
)
LANGUAGE_CODE = 'pl'

USE_I18N = True
USE_L10N = False
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale')
)

DATE_FORMAT = 'd-m-y'
DATETIME_FORMAT = 'd-m-y H:i'
DECIMAL_SEPARATOR = '.'
FIRST_DAY_OF_WEEK = 1
NUMBER_GROUPING = 1
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '


#####################
#   Static files    #
#####################

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = SITE_URL + '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = SITE_URL + '/static/'

STATICFILES_DIRS = [
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#################
#   Templates   #
#################

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS += [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
]

TEMPLATE_DIRS += [
    os.path.join(BASE_DIR, 'templates'),
]
#############
#   Apps    #
#############

MIDDLEWARE_CLASSES += [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

#############
#    CMS    #
#############

MIDDLEWARE_CLASSES += {
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
}

TEMPLATE_CONTEXT_PROCESSORS += [
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.cms_settings',
]

CMS_TEMPLATES = (
    ('conferences/cms/base.html', 'Basic template'),
)

#########################
#   Session Security    #
#########################

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_EXPIRE_AFTER = 900
SESSION_SECURITY_WARN_AFTER = 840
MIDDLEWARE_CLASSES += [
    'session_security.middleware.SessionSecurityMiddleware',
]

#####################
#   Debug Toolbar   #
#####################

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {

}


def uniquify(seq):
    '''
    Removes duplicates from list
    '''
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


try:
    from local_settings import *
except ImportError:
    pass

TEMPLATE_DIRS = uniquify(TEMPLATE_DIRS)
# INSTALLED_APPS = uniquify(INSTALLED_APPS)
TEMPLATE_CONTEXT_PROCESSORS = uniquify(TEMPLATE_CONTEXT_PROCESSORS)
MIDDLEWARE_CLASSES = uniquify(MIDDLEWARE_CLASSES)