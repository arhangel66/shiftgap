# -*- coding: utf8 -*-
from django.template.loader import render_to_string
from apps.shifts.views import ShiftListing

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from django.test import TestCase, Client, RequestFactory


class Shifts3Test(TestCase):
    base_url = '/'

    def test_return_exception(self):
        self.assertEqual(True, False)
