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
        UserAccount.objects.all().delete()
        self.count_users = 3
        self.shifts = gen_fake_shifts(self.count_shifts, gen_fake_users(self.count_users-1), start=get_list_days_of_week()[0])
        self.username = 'admin'
        self.password = 'secret'
        self.user = UserAccount.objects.create_user(self.username, 'mail@example.com', self.password)
        self.user.is_staff = True
        # self.user.is_superuser = True
        self.user.save()
        self.myshifts = gen_fake_shifts(self.count_shifts,[self.user], start=get_list_days_of_week()[0])


    def test_get_dates(self):
        # request_factory = RequestFactory()
        # request = request_factory.get('/shifts')
        view = ShiftListing()
        res = view.get_dates()
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 7)
        self.assertEqual(len(res[1]), 7)
        self.assertEqual(type(res[0][1]), type(''))
        self.assertEqual(type(res[1]), dict)
        self.assertEqual(type(list(res[1].values())[0]), type(''))

    # def test_get_users(self):
    #     view = ShiftListing()
    #     res = view.get_users(view.get_queryset())
    #     self.assertEqual(len(res), 2)
    #     self.assertEqual(len(res[0]), self.count_users)
    #     self.assertEqual(len(res[1]), self.count_users)
    #     self.assertEqual(type(res[0][1]), int)
    #     self.assertEqual(type(res[1]), dict)
    #     self.assertEqual(type(list(res[1].values())[0]), str)

    def test_get_weeks(self):
        view = ShiftListing()
        res = view.get_weeks()
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 4)
        self.assertEqual(len(res[1]), 4)

    def test_get_days_of_week(self):
        view = ShiftListing()
        res = view.get_days_of_week()
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 7)
        self.assertEqual(len(res[1]), 7)

    def test_modal_create(self):
        c = Client()
        response = c.get(reverse('shifts:shift_create'))
        self.assertEquals(response.status_code, 302)
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('shifts:shift_list'))
        self.assertEquals(response.status_code, 200)

    def test_modal_update(self):
        c = Client()
        print(self.shifts[0].id)
        response = c.get(reverse('shifts:shift_update', args=[self.shifts[0].id]))
        self.assertEquals(response.status_code, 302)
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('shifts:shift_update', args=[self.shifts[0].id]))
        self.assertEquals(response.status_code, 200)

    def test_modal_update_permission(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('shifts:shift_update', args=[self.shifts[0].id]))
        self.assertEquals(len(response.content.strip()), len(str("You can't Update this shift")))

        response = c.get(reverse('shifts:shift_update', args=[self.myshifts[0].id]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.content.strip()) > 100, True)

    def test_modal_delete_permission(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('shifts:shift_delete', args=[self.shifts[0].id]))
        self.assertEquals(len(response.content.strip()), len(str("You can't Delete this shift")))

        response = c.post(reverse('shifts:shift_delete', args=[self.myshifts[0].id]))
        self.assertEquals(response.status_code, 302)
