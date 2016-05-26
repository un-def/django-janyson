# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from .descriptors import JanySONDescriptor
from .options import Options
from .utils import setdefaultattr
if six.PY2:
    from .utils import dir_py2


__all__ = ['add_fields']


def dir_override(self):
    dir_orig = getattr(self, '_jnsn_dir_orig', None)
    if dir_orig:
        dir_list = dir_orig()
    else:
        dir_list = dir_py2(self) if six.PY2 else super().__dir__()
    for field in self._jnsn_dir_hidden_fields:
        if not hasattr(self, field):
            try:
                dir_list.remove(field)
            except ValueError:   # pragma: no cover
                pass
    return dir_list


def add_fields(fields, field_options=None, janyson_field='janyson'):
    def decorator(cls):
        setdefaultattr(cls, '_jnsn_fields', {})
        setdefaultattr(cls, '_jnsn_settings', {})
        cls._jnsn_settings.setdefault('janyson_field', janyson_field)
        if isinstance(fields, dict):
            fields_is_dict = True
        elif isinstance(fields, (list, tuple)):
            fields_is_dict = False
            if not isinstance(field_options, dict):
                raise ValueError("specify common field options "
                                 "with 'field_options' argument")
            options = field_options.copy()
        else:
            raise TypeError("'fields' must be dict, list, or tuple")
        hidden_fields = []
        for field in fields:
            if fields_is_dict:
                if field_options:
                    options = field_options.copy()
                    options.update(fields[field])
                else:
                    options = fields[field].copy()
            cls._jnsn_fields[field] = options
            options_obj = Options(options)
            if options_obj.dir_hide:
                hidden_fields.append(field)
            setattr(cls, field, JanySONDescriptor(field, options_obj))
        if hidden_fields:
            if hasattr(cls, '_jnsn_dir_hidden_fields'):
                cls._jnsn_dir_hidden_fields.extend(hidden_fields)
            else:
                cls._jnsn_dir_hidden_fields = hidden_fields
                dir_orig = getattr(cls, '__dir__', None)
                if dir_orig:
                    cls._jnsn_dir_orig = dir_orig
                cls.__dir__ = dir_override
        return cls
    return decorator
