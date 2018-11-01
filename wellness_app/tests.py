# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .processes import decodeData
# Create your tests here.

class dataEncodeTestCase(TestCase):
    def setUp(self):
        pass

    def test_decode_data(self):
        self.assertEqual(decodeData('\x88'), [8, 8])
        self.assertEqual(decodeData('\x08\x88\x11'), [8, 8, 8, 1, 1])
        self.assertEqual(decodeData('\x88\x88\xa1\x1a'), [8, 8, 8, 8, None, 1, 1, None])
