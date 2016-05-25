# -*- coding: utf-8 -*-

from django.test import TestCase

from .models import Item


class StoredValuesTestCase(TestCase):

    def setUp(self):
        item = Item.objects.create(name='test item')
        item.test_num = 10
        item.test_str = 'some text'
        item.test_bool = True
        item.test_nullbool = True
        item.save()
        self.item = Item.objects.get(pk=item.pk)

    def test_num_stored_value(self):
        self.assertEqual(self.item.test_num, 10)

    def test_str_stored_value(self):
        self.assertEqual(self.item.test_str, 'some text')

    def test_bool_stored_value(self):
        self.assertIs(self.item.test_bool, True)

    def test_nullbool_stored_value(self):
        self.assertIs(self.item.test_nullbool, True)


class DefaultValuesTestCase(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name='test item')

    def test_num_default_value(self):
        self.assertEqual(self.item.test_num, 0)

    def test_str_default_value(self):
        self.assertEqual(self.item.test_str, 'default text')

    def test_bool_default_value(self):
        self.assertIs(self.item.test_bool, False)

    def test_nullbool_default_value(self):
        self.assertIsNone(self.item.test_nullbool)
