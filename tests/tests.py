# -*- coding: utf-8 -*-

from imp import reload

from django.test import TestCase

from janyson import add_fields

from . import models


def add_fields_to_item_model(*args, **kwargs):
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


class StoredValuesTestCase(TestCase):

    JANYSON_FIELD = None

    @classmethod
    def setUpClass(cls):
        super(StoredValuesTestCase, cls).setUpClass()
        kwargs = {}
        if cls.JANYSON_FIELD:
            kwargs['janyson_field'] = cls.JANYSON_FIELD
        add_fields_to_item_model(FIELDS_WITHOUT_DEFAULT_VALUES, **kwargs)
        item = models.Item.objects.create(name='test item')
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
        item = models.Item.objects.create(name='test item')
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
        item = models.Item.objects.create(name='test item')
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
