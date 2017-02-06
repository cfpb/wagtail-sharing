from __future__ import absolute_import, unicode_literals

import os


SECRET_KEY = 'not needed'

ROOT_URLCONF = 'wagtailsharing.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DATABASE_ENGINE',
            'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('DATABASE_NAME', 'wagtailsharing'),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASS', None),
        'HOST': os.environ.get('DATABASE_HOST', None),

        'TEST': {
            'NAME': os.environ.get('DATABASE_NAME', None),
        },
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'taggit',
    'wagtail.tests.testapp',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',

    'wagtailsharing',
)
