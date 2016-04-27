# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

import six
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.forms import JSONField


__all__ = ['JanySONField']


class JanySONField(JSONField):
    default_error_messages = {
        'invalid': _("JSON deserialization error: %(error)s"),
        'invalid_json_type': _("Invalid JSON type"),
        'invalid_value': _("%(field)s (%(type)s)"
                           " - invalid value: %(value)s"),
        'non_declared_fields': _("Non-declared field(s): %(fields)s"),
    }

    def to_python(self, value):
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            return json.loads(value)
        except ValueError as error:
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'error': error},
            )

    def prepare_value(self, value):
        if isinstance(value, six.text_type):
            return value
        return json.dumps(
            value,
            ensure_ascii=False,
            indent=4,
            separators=(',', ': '),
            sort_keys=True
        )
