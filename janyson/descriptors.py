# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.apps import apps
from django.db.models import QuerySet

from .options import Options
from .validators import validators
from .utils import setdefaultattr


__all__ = ['BaseJanySONDescriptor', 'JanySONDescriptor']


class BaseJanySONDescriptor(object):

    errors = {
        'invalid_json_type': "invalid JSON type {type} "
                             "(must be dict or None)",
        'invalid_value': "invalid value '{value}' for "
                         "'{field}' ({type}) field",
        'no_pk': "{instance} has no pk (do you save() it first?)",
        'fk_invalid': "value must be positive integer (primary key) "
                      "or {model} instance",
        'm2m_invalid': "value must be list or tuple of integers "
                       "(primary keys) or {model} instances or "
                       "{model} QuerySet"
    }

    def __init__(self, field, options):
        self.field = field
        if not isinstance(options, Options):
            options = Options(options)   # pragma: no cover
        self.options = Options(options)

    def _get_value(self, obj):
        json_dict = self._get_json_dict(obj)
        if self.field in json_dict:
            value = json_dict[self.field]
        elif self.options.use_default:
            value = self.options.default
        else:
            self._raise_attribute_error(obj)
        if self.options.type == 'fk' and self.options.use_instance:
            value = self._get_model_instance(obj, value)
        elif self.options.type == 'm2m' and self.options.use_instance:
            value = self._get_model_queryset(obj, value)
        return value

    def _set_value(self, obj, value):
        json_dict = self._get_json_dict(obj, set_if_none=True)
        error = None
        type_ = self.options.type
        if not validators[type_](value):
            error = self.errors['invalid_value'].format(
                value=repr(value), field=self.field, type=type_)
            if type_ in ('fk', 'm2m') and self.options.use_instance:
                model = self._get_model()
                if type_ == 'fk':
                    if not isinstance(value, model):
                        error += "; "+self.errors['fk_invalid'].format(
                            model=model.__name__)
                    else:
                        if not value.pk:
                            error += "; "+self.errors['no_pk'].format(
                                instance=repr(value))
                        else:
                            value = value.pk
                            error = None
                elif type_ == 'm2m':
                    error_invalid = "; "+self.errors['m2m_invalid'].format(
                            model=model.__name__)
                    if isinstance(value, (list, tuple)):
                        if not all(isinstance(e, model) for e in value):
                            error += error_invalid
                        else:
                            pks = []
                            for instance in value:
                                if not instance.pk:
                                    error += "; "+self.errors['no_pk'].format(
                                        instance=repr(instance))
                                    break
                                else:
                                    pks.append(instance.pk)
                            else:
                                value = pks
                                error = None
                    elif isinstance(value, QuerySet) and value.model == model:
                        value = [i.pk for i in value]
                        error = None
                    else:
                        error += error_invalid
        if error:
            raise TypeError(error)
        if (type_ in ('list', 'm2m') and
                not isinstance(value, six.string_types)):
            value = list(value)
        json_dict[self.field] = value

    def _delete_value(self, obj):
        json_dict = self._get_json_dict(obj)
        if self.field in json_dict:
            del json_dict[self.field]
        else:
            self._raise_attribute_error(obj)

        if not hasattr(obj, '_jnsn_cache'):
            return
        if self.options.type == 'fk':
            obj._jnsn_cache.pop(self.field+'_instance', None)
        elif self.options.type == 'm2m':
            obj._jnsn_cache.pop(self.field+'_queryset', None)
            obj._jnsn_cache.pop(self.field+'_set', None)

    def _get_json_dict(self, obj, set_if_none=False):
        janyson_field = obj._jnsn_settings['janyson_field']
        json_dict = getattr(obj, janyson_field)
        if json_dict is None:
            json_dict = {}
            if set_if_none:
                setattr(obj, janyson_field, json_dict)
        if isinstance(json_dict, dict):
            return json_dict
        else:
            error = self.errors['invalid_json_type'].format(
                type=type(json_dict))
            raise TypeError(error)

    def _get_model(self):
        model = self.options.model
        if isinstance(model, six.string_types):
            model = apps.get_model(model)
            self.options.model = model
        return model

    def _get_model_instance(self, obj, pk):
        setdefaultattr(obj, '_jnsn_cache', {})
        instance_key = self.field + '_instance'
        instance = obj._jnsn_cache.get(instance_key)
        if instance is not None and instance.pk == pk:
            return instance
        model = self._get_model()
        instance = model.objects.get(pk=pk)
        obj._jnsn_cache[instance_key] = instance
        return instance

    def _get_model_queryset(self, obj, pks):
        pks_set = set(pks)
        setdefaultattr(obj, '_jnsn_cache', {})
        queryset_key = self.field + '_queryset'
        set_key = self.field + '_set'
        queryset = obj._jnsn_cache.get(queryset_key)
        if queryset is not None and obj._jnsn_cache[set_key] == pks_set:
            return queryset
        obj._jnsn_cache[set_key] = pks_set
        model = self._get_model()
        if pks == '*':
            queryset = model.objects.all()
        elif not pks:
            queryset = model.objects.none()
        elif pks[0] > 0:
            queryset = model.objects.filter(pk__in=pks)
        else:
            queryset = model.objects.exclude(pk__in=[abs(e) for e in pks])
        obj._jnsn_cache[queryset_key] = queryset
        return queryset

    def _raise_attribute_error(self, obj):
        raise AttributeError("'{}' object has no attribute '{}'".format(
            obj.__class__.__name__, self.field))


class JanySONDescriptor(BaseJanySONDescriptor):

    def __get__(self, obj, objtype):
        return self._get_value(obj)

    def __set__(self, obj, value):
        self._set_value(obj, value)

    def __delete__(self, obj):
        self._delete_value(obj)
