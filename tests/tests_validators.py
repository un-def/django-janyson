
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
from functools import partial

from django.test import TestCase

from janyson.validators import validators


class ValidatorsTestCase(TestCase):

    TEST_VALUES = {
        'str': 'string',
        'unicode': 'über',
        'pos_int': 123,
        'neg_int': -123,
        'zero': 0,
        'float': .45,
        'true': True,
        'false': False,
        'none': None,
        'list': [0, 1, 2],
        'tuple': (3, 4, 'foo', True),
        'dict': {'foo': 'bar'},
        'asterisk': '*',
        'pos_int_list': [1, 3, 7],
        'neg_int_list': [-1, -3, -7],
        'mixed_int_list': [1, 3, -7],
    }

    RE_METHOD = re.compile('^run_(\w+)_validator_test$')

    def __getattr__(self, attr):
        mo = self.RE_METHOD.match(attr)
        if mo:
            return partial(self._run_validator_test, mo.group(1))
        raise AttributeError(attr)

    def _run_validator_test(self, validator_type, *allowed_value_names):
        for value_name, value in self.TEST_VALUES.items():
            if value_name in allowed_value_names:
                assert_method = self.assertTrue
            else:
                assert_method = self.assertFalse
            assert_method(
                validators[validator_type](value),
                "'{}' validator error with value '{}' ({})".format(
                    validator_type, value, value_name))

    def test_str_validator(self):
        self.run_str_validator_test('str', 'unicode', 'asterisk')

    def test_num_validator(self):
        self.run_num_validator_test('pos_int', 'neg_int', 'zero', 'float')

    def test_bool_validator(self):
        self.run_bool_validator_test('true', 'false')

    def test_nullbool_validator(self):
        self.run_nullbool_validator_test('true', 'false', 'none')

    def test_list_validator(self):
        self.run_list_validator_test('list', 'pos_int_list', 'neg_int_list',
                                     'mixed_int_list', 'tuple')

    def test_dict_validator(self):
        self.run_dict_validator_test('dict')

    def test_fk_validator(self):
        self.run_fk_validator_test('pos_int')

    def test_m2m_validator(self):
        self.run_m2m_validator_test('asterisk', 'pos_int_list',
                                    'neg_int_list',)
