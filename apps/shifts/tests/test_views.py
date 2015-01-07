# -*- coding: utf8 -*-
import datetime
from apps.shifts.tests.fake import gen_fake_users, gen_fake_shifts

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory, Client
from apps.shifts.models import Shift, UserAccount
from apps.shifts.views import ShiftListing, get_list_days_of_week


class ShiftListingFuncsTest(TestCase):

    def setUp(self):
        self.count_shifts = 10
        self.count_users = 3
        self.shifts = gen_fake_shifts(self.count_shifts, gen_fake_users(self.count_users), start=get_list_days_of_week()[0])
        self.username = 'admin'
        self.password = 'secret'
        self.user = UserAccount.objects.create_user(self.username, 'mail@example.com', self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()


    def test_get_dates(self):
        # request_factory = RequestFactory()
        # request = request_factory.get('/shifts')
        view = ShiftListing()
        res = view.get_dates()
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 8)
        self.assertEqual(len(res[1]), 7)
        self.assertEqual(type(res[0][1]), type(''))
        self.assertEqual(type(res[1]), dict)
        self.assertEqual(type(list(res[1].values())[0]), type(''))

    def test_get_users(self):
        view = ShiftListing()
        res = view.get_users(view.get_queryset())
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), self.count_users+1)
        self.assertEqual(len(res[1]), self.count_users)
        self.assertEqual(type(res[0][1]), int)
        self.assertEqual(type(res[1]), dict)
        self.assertEqual(type(list(res[1].values())[0]), type(UserAccount()))

    def test_modal_create(self):
        c = Client()
        response = c.get(reverse('shifts:shift_create'))
        self.assertEquals(response.status_code, 302)
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('shifts:shift_list'))
        self.assertEquals(response.status_code, 200)

