# -*- coding: utf-8 -*-

from django.db import models

from janyson.fields import JanySONField
from janyson import add_fields


fields = {
    'test_num': {
        'type': 'num',
        'use_default': True,
        'default': 0,
    },
    'test_str': {
        'type': 'str',
        'use_default': True,
        'default': 'default text'
    },
    'test_bool': {
        'type': 'bool',
        'use_default': True,
        'default': False,
    },
    'test_nullbool': {
        'type': 'bool',
        'use_default': True,
        'default': None,
    },
}


@add_fields(fields)
class Item(models.Model):

    name = models.SlugField(max_length=16)
    janyson = JanySONField(default=dict, blank=True, null=True)
