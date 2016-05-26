# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def setdefaultattr(obj, name, value):
    if not hasattr(obj, name):
        setattr(obj, name, value)


def _get_attrs(obj):
    from types import DictProxyType
    if not hasattr(obj, '__dict__'):   # pragma: no cover
        return []   # slots only
    if not isinstance(obj.__dict__,
                      (dict, DictProxyType)):   # pragma: no cover
        raise TypeError("{}.__dict__ is not a dictionary".format(
            obj.__name__))
    return obj.__dict__.keys()


# https://stackoverflow.com/questions/
# 15507848/the-correct-way-to-override-the-dir-method-in-python
def dir_py2(obj):
    attrs = set()
    if not hasattr(obj, '__bases__'):   # obj is an instance
        if not hasattr(obj, '__class__'):   # slots
            return sorted(_get_attrs(obj))   # pragma: no cover
        cls = obj.__class__
        attrs.update(_get_attrs(cls))
    else:   # obj is a class
        cls = obj
    for base_cls in cls.__bases__:
        attrs.update(_get_attrs(base_cls))
        attrs.update(dir_py2(base_cls))
    attrs.update(_get_attrs(obj))
    return sorted(attrs)
