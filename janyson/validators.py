# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six


__all__ = ['validators']


def list_validator(value):
    if isinstance(value, six.string_types):
        return value == '*'
    return isinstance(value, (list, tuple))


def m2m_validator(value):
    if isinstance(value, six.string_types):
        return value == '*'
    if not isinstance(value, (list, tuple)):
        return False
    if not all(isinstance(e, int) and not isinstance(e, bool) for e in value):
        return False
    if not (all(e > 0 for e in value) or all(e < 0 for e in value)):
        return False
    return True


validators = {
    'str': lambda v: isinstance(v, six.string_types),
    'num': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    'bool': lambda v: isinstance(v, bool),
    'nullbool': lambda v: v is None or isinstance(v, bool),
    'list': list_validator,
    'dict': lambda v: isinstance(v, dict),
    'fk': lambda v: isinstance(v, int) and not isinstance(v, bool) and v > 0,
    'm2m': m2m_validator,
}
