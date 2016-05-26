# -*- coding: utf-8 -*-

from django.test import TestCase

from janyson.options import Options


class OptionsTestCase(TestCase):

    def setUp(self):
        self.options = Options()

    def test_default_options(self):
        for option, value in Options.default_options.items():
            self.assertEqual(getattr(self.options, option), value)

    def test_get_nonexistent(self):
        with self.assertRaisesRegexp(AttributeError, "Missing option"):
            self.options.key

    def test_set_and_get(self):
        self.options.key = 'value'
        self.assertEqual(self.options.key, 'value')

    def test_set_and_delete(self):
        self.options.key = 'value'
        del self.options.key
        with self.assertRaisesRegexp(AttributeError, "Missing option"):
            self.options.key

    def test_delete_nonexistent(self):
        with self.assertRaisesRegexp(AttributeError, "Missing option"):
            del self.options.key
