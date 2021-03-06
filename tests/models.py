# -*- coding: utf-8 -*-

from django.db import models

from janyson.fields import JanySONField


class Item(models.Model):

    name = models.SlugField(max_length=32)
    janyson = JanySONField(default=dict, blank=True, null=True)
    another_janyson = JanySONField(blank=True, null=True)


class Tag(models.Model):

    name = models.SlugField(max_length=32)

    class Meta:
        ordering = ['name']


class AnotherModel(models.Model):

    name = models.SlugField(max_length=32)
