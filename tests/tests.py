# -*- coding: utf-8 -*-

from django.test import TestCase

from janyson import add_fields

from .models import Item


def add_fields_to_item_model(fields):
    add_fields(fields)(Item)


fields_without_default_values = {
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
}

fields_with_default_values = {
    'test_num': {
        'type': 'num',
        'use_default': True,
        'default': 0,
    },
    'test_str': {
        'type': 'str',
        'use_default': True,
        'default': 'default text'
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
}


class StoredValuesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(StoredValuesTestCase, cls).setUpClass()
        add_fields_to_item_model(fields_without_default_values)
        item = Item.objects.create(name='test item')
        item.test_num = 10
        item.test_str = 'some text'
        item.test_bool = True
        item.test_nullbool = True
        item.save()
        cls.item_pk = item.pk

    def setUp(self):
        self.item = Item.objects.get(pk=self.item_pk)

    def test_num_stored_value(self):
        self.assertEqual(self.item.test_num, 10)

    def test_str_stored_value(self):
        self.assertEqual(self.item.test_str, 'some text')

    def test_bool_stored_value(self):
        self.assertIs(self.item.test_bool, True)

    def test_nullbool_stored_value(self):
        self.assertIs(self.item.test_nullbool, True)


class DefaultValuesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DefaultValuesTestCase, cls).setUpClass()
        add_fields_to_item_model(fields_with_default_values)
        item = Item.objects.create(name='test item')
        cls.item_pk = item.pk

    def setUp(self):
        self.item = Item.objects.get(pk=self.item_pk)

    def test_num_default_value(self):
        self.assertEqual(self.item.test_num, 0)

    def test_str_default_value(self):
        self.assertEqual(self.item.test_str, 'default text')

    def test_bool_default_value(self):
        self.assertIs(self.item.test_bool, False)

    def test_nullbool_default_value(self):
        self.assertIsNone(self.item.test_nullbool)


class NoDefaultValuesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(NoDefaultValuesTestCase, cls).setUpClass()
        add_fields_to_item_model(fields_without_default_values)
        item = Item.objects.create(name='test item')
        cls.item_pk = item.pk

    def setUp(self):
        self.item = Item.objects.get(pk=self.item_pk)

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
