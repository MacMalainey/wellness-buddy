# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Tip
from .processes import decodeData, getResponseType
# Create your tests here.

class DataEncodeTestCase(TestCase):
    def setUp(self):
        pass

    def test_decode_data(self):
        self.assertEqual(decodeData('\x88'), [8, 8])
        self.assertEqual(decodeData('\x08\x88\x11'), [8, 8, 8, 1, 1])
        self.assertEqual(decodeData('\x88\x88\xa1\x1a'), [8, 8, 8, 8, None, 1, 1, None])

class ResponseTypeTestCase(TestCase):
    def setUp(self):
        for x in [
            Tip.LEVEL_CRITICAL, Tip.LEVEL_GOOD, Tip.LEVEL_LOW,
            Tip.LEVEL_MEDIUM, Tip.LEVEL_NONE
        ]:
            Tip.objects.create(message="", level=x)
            Tip.objects.create(message="", level=x)

    def test_response_level(self):
        self.assertEqual(
            getResponseType([0, None, None]).level,
            Tip.LEVEL_CRITICAL
        )
        self.assertEqual(
            getResponseType([0, 7, 5]).level,
            Tip.LEVEL_CRITICAL
        )
        self.assertEqual(
            getResponseType([7]).level,
            Tip.LEVEL_NONE
        )
        self.assertEqual(
            getResponseType([7, None, None, None, None, None, None, None]).level,
            Tip.LEVEL_NONE
        )
        self.assertEqual(
            getResponseType([2, 6, 6]).level,
            Tip.LEVEL_CRITICAL
        )
        self.assertEqual(
            getResponseType([3, 8, 2]).level,
            Tip.LEVEL_LOW
        )
        self.assertEqual(
            getResponseType([5, 8, 2]).level,
            Tip.LEVEL_MEDIUM
        )
        self.assertEqual(
            getResponseType([8, 8, 2]).level,
            Tip.LEVEL_GOOD
        )

