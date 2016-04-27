# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField

from . import forms


__all__ = ['JanySONField']


class JanySONField(JSONField):

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.JanySONField}
        defaults.update(kwargs)
        return super(JanySONField, self).formfield(**defaults)
