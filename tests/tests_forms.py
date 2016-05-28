# -*- coding: utf-8 -*-

from django.test import TestCase
from django.forms import modelform_factory, ValidationError

from janyson.forms import JanySONField

from .models import Item


class FormFieldTestCase(TestCase):

    ItemForm = modelform_factory(Item, fields=['janyson'])

    def test_to_python_valid_value(self):
        field = JanySONField()
        value = field.clean('{"foo": "bar", "baz": true}')
        self.assertEqual(value, {'foo': 'bar', 'baz': True})

    def test_to_python_invalid_value(self):
        field = JanySONField()
        with self.assertRaisesRegexp(
                ValidationError, "deserialization error"):
            field.clean('{"foo": bar')

    def test_to_python_empty_value(self):
        field = JanySONField(required=False)
        value = field.clean('')
        self.assertIsNone(value)

    def test_prepare_value(self):
        form = self.ItemForm({'janyson': '[1, "foo", true]'})
        self.assertIn('true\n]</textarea>', form.as_p())

    def test_prepare_value_string_no_quotes(self):
        form = self.ItemForm({'janyson': '"foo"'})
        self.assertIn('foo</textarea>', form.as_p())
