# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Options(dict):

    default_options = {
        'use_default': False,
        'default': None,
        'use_instance': True,
        'dir_hide': False,
    }

    def __getattr__(self, name):
        if name in self:
            return self[name]
        if name in self.__class__.default_options:
            return self.__class__.default_options[name]
        self._raise_attribute_error(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            self._raise_attribute_error(name)

    @staticmethod
    def _raise_attribute_error(option):
        raise AttributeError("Missing option '{}'".format(option))
