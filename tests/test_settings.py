# -*- coding: utf-8 -*-

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'tests',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'not-used',
        'TEST': {},
    },
}
