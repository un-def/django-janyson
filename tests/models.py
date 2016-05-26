# -*- coding: utf-8 -*-

from django.db import models

from janyson.fields import JanySONField


class Item(models.Model):

    name = models.SlugField(max_length=32)
    janyson = JanySONField(default=dict, blank=True, null=True)
    another_janyson = JanySONField(default=dict, blank=True, null=True)
