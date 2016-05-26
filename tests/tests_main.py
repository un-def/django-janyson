# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from imp import reload

from django.test import TestCase

from janyson import add_fields

from . import models


def add_fields_to_item_model(*args, **kwargs):
    if not kwargs.pop('no_reload', False):
        reload(models)
    add_fields(*args, **kwargs)(models.Item)


TEST_NUM = 10
TEST_STR = 'some text'
TEST_LIST = [1, 3, 5]
TEST_DICT = {'a': 'boo', 'b': 3, 'c': True}

TEST_NUM_DEFAULT = 3
TEST_STR_DEFAULT = 'default text'
TEST_LIST_DEFAULT = [1, 2]
TEST_DICT_DEFAULT = {'foo': 'bar', 'baz': None}


FIELDS_WITHOUT_DEFAULT_VALUES = {
    'test_num': {
        'type': 'num',
    },
    'test_str': {
        'type': 'str',
    },
    'test_bool': {
        'type': 'bool',
        'use_default': False,
        'default': False,
    },
    'test_nullbool': {
        'type': 'bool',
        'use_default': False,
    },
    'test_list': {
        'type': 'list',
    },
    'test_dict': {
        'type': 'dict',
    },
}

FIELDS_WITH_DEFAULT_VALUES = {
    'test_num': {
        'type': 'num',
        'use_default': True,
        'default': TEST_NUM_DEFAULT,
    },
    'test_str': {
        'type': 'str',
        'use_default': True,
        'default': TEST_STR_DEFAULT,
    },
    'test_bool': {
        'type': 'bool',
        'use_default': True,
        'default': False,
    },
    'test_nullbool': {
        'type': 'bool',
        'use_default': True,
    },
    'test_list': {
        'type': 'list',
        'use_default': True,
        'default': TEST_LIST_DEFAULT,
    },
    'test_dict': {
        'type': 'dict',
        'use_default': True,
        'default': TEST_DICT_DEFAULT,
    },
}

FIELDS_DIR_HIDE_DEFAULT = {
    'test_default_hide': {
        'type': 'str',
        'use_default': True,
        'default': TEST_STR_DEFAULT,
        'dir_hide': True,
    },
    'test_default_no_hide': {
        'type': 'str',
        'use_default': True,
        'default': TEST_STR_DEFAULT,
        'dir_hide': False,
    },
}

FIELDS_DIR_HIDE_NO_DEFAULT = {
    'test_no_default_hide': {
        'type': 'str',
        'use_default': False,
        'dir_hide': True,
    },
    'test_no_default_no_hide': {
        'type': 'str',
        'use_default': False,
        'dir_hide': False,
    },
}

COMMON_FIELD_OPTIONS = {
    'type': 'str',
    'use_default': True,
    'default': TEST_STR_DEFAULT,
}

COMMON_FIELDS_OVERRIDE = {
    'str1': {},
    'str2': {
        'use_default': False,
    },
    'num': {
        'type': 'num',
        'default': TEST_NUM_DEFAULT
    }
}


class StoredValuesTestCase(TestCase):

    JANYSON_FIELD = None

    @classmethod
    def setUpClass(cls):
        super(StoredValuesTestCase, cls).setUpClass()
        kwargs = {}
        if cls.JANYSON_FIELD:
            kwargs['janyson_field'] = cls.JANYSON_FIELD
        add_fields_to_item_model(FIELDS_WITHOUT_DEFAULT_VALUES, **kwargs)
        item = models.Item.objects.create(name='stored_values')
        item.test_num = TEST_NUM
        item.test_str = TEST_STR
        item.test_bool = True
        item.test_nullbool = True
        item.test_list = TEST_LIST
        item.test_dict = TEST_DICT
        item.save()
        cls.item_pk = item.pk

    def setUp(self):
        self.item = models.Item.objects.get(pk=self.item_pk)

    def test_num_stored_value(self):
        self.assertEqual(self.item.test_num, TEST_NUM)

    def test_str_stored_value(self):
        self.assertEqual(self.item.test_str, TEST_STR)

    def test_bool_stored_value(self):
        self.assertIs(self.item.test_bool, True)

    def test_nullbool_stored_value(self):
        self.assertIs(self.item.test_nullbool, True)

    def test_list_stored_value(self):
        self.assertListEqual(self.item.test_list, TEST_LIST)

    def test_dict_stored_value(self):
        self.assertDictEqual(self.item.test_dict, TEST_DICT)


class StoredValuesInAnotherJanySONFieldTestCase(StoredValuesTestCase):

    JANYSON_FIELD = 'another_janyson'


class DefaultValuesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DefaultValuesTestCase, cls).setUpClass()
        add_fields_to_item_model(FIELDS_WITH_DEFAULT_VALUES)
        item = models.Item.objects.create(name='default_values')
        cls.item_pk = item.pk

    def setUp(self):
        self.item = models.Item.objects.get(pk=self.item_pk)

    def test_num_default_value(self):
        self.assertEqual(self.item.test_num, TEST_NUM_DEFAULT)

    def test_str_default_value(self):
        self.assertEqual(self.item.test_str, TEST_STR_DEFAULT)

    def test_bool_default_value(self):
        self.assertIs(self.item.test_bool, False)

    def test_nullbool_default_value(self):
        self.assertIsNone(self.item.test_nullbool)

    def test_list_default_value(self):
        self.assertListEqual(self.item.test_list, TEST_LIST_DEFAULT)

    def test_dict_default_value(self):
        self.assertDictEqual(self.item.test_dict, TEST_DICT_DEFAULT)


class NoDefaultValuesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(NoDefaultValuesTestCase, cls).setUpClass()
        add_fields_to_item_model(FIELDS_WITHOUT_DEFAULT_VALUES)
        item = models.Item.objects.create(name='no_default_values')
        cls.item_pk = item.pk

    def setUp(self):
        self.item = models.Item.objects.get(pk=self.item_pk)

    def test_num_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_num

    def test_str_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_str

    def test_bool_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_bool

    def test_nullbool_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_nullbool

    def test_list_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_list

    def test_dict_no_default_value_error(self):
        with self.assertRaises(AttributeError):
            self.item.test_dict


class DirHideTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DirHideTestCase, cls).setUpClass()
        add_fields_to_item_model(FIELDS_DIR_HIDE_DEFAULT)
        add_fields_to_item_model(FIELDS_DIR_HIDE_NO_DEFAULT, no_reload=True)

    def setUp(self):
        self.item = models.Item(name='dir_hide')

    def test_no_value_no_default_no_hide(self):
        self.assertIn('test_no_default_no_hide', dir(self.item))

    def test_no_value_no_default_hide(self):
        self.assertNotIn('test_no_default_hide', dir(self.item))

    def test_value_no_hide(self):
        self.item.test_no_default_no_hide = 'foo'
        self.assertIn('test_no_default_no_hide', dir(self.item))

    def test_value_hide(self):
        self.item.test_no_default_hide = 'foo'
        self.assertIn('test_no_default_hide', dir(self.item))

    def test_default_no_hide(self):
        self.assertIn('test_default_no_hide', dir(self.item))

    def test_default_hide(self):
        self.assertIn('test_default_hide', dir(self.item))


class CommonFieldOptionsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(CommonFieldOptionsTestCase, cls).setUpClass()
        add_fields_to_item_model(
            COMMON_FIELDS_OVERRIDE, field_options=COMMON_FIELD_OPTIONS)

    def setUp(self):
        self.item = models.Item(name='common_field_options')

    def test_no_override(self):
        self.assertEqual(self.item.str1, TEST_STR_DEFAULT)

    def test_override_use_default(self):
        with self.assertRaises(AttributeError):
            self.item.str2

    def test_override_type_and_default(self):
        self.assertEqual(self.item.num, TEST_NUM_DEFAULT)


class AcceptableFieldsArgTypesTestCase(TestCase):

    def test_fields_as_dict_without_common_fields_options(self):
        add_fields_to_item_model(COMMON_FIELDS_OVERRIDE)
        item = models.Item(name='fields_as_dict')
        item.num = TEST_NUM
        self.assertEqual(item.num, TEST_NUM)

    def test_fields_as_dict_with_common_fields_options(self):
        add_fields_to_item_model(
            COMMON_FIELDS_OVERRIDE, field_options=COMMON_FIELD_OPTIONS)
        item = models.Item(name='fields_as_dict_with_common')
        self.assertEqual(item.str1, TEST_STR_DEFAULT)

    def test_fields_as_list_without_common_fields_options(self):
        with self.assertRaisesRegexp(ValueError, "common field options"):
            add_fields_to_item_model(['str1', 'str2'])

    def test_fields_as_list_with_common_fields_options(self):
        add_fields_to_item_model(
            ['str1', 'str2'], field_options=COMMON_FIELD_OPTIONS)
        item = models.Item(name='fields_as_list_with_common')
        item.str2 = TEST_STR
        self.assertEqual(item.str1, TEST_STR_DEFAULT)
        self.assertEqual(item.str2, TEST_STR)

    def test_fields_as_str_with_common_fields_options(self):
        with self.assertRaisesRegexp(TypeError, "'fields' must be"):
            add_fields_to_item_model(
                'str1', field_options=COMMON_FIELD_OPTIONS)
