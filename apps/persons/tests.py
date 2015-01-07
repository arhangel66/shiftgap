# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse
from apps.persons.views import UserCreate
from apps.shifts.models import UserAccount

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'


from django.template.loader import render_to_string
from apps.shifts.tests.fake import gen_fake_users, gen_fake_organizations, gen_fake_shifts
from apps.shifts.views import ShiftListing

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from django.test import TestCase, Client, RequestFactory


class PersonsTest(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'secret'
        self.user = UserAccount.objects.create_user(self.username, 'mail@example.com', self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def test_returns_correct_html(self):
        request_factory = RequestFactory()
        request = request_factory.get(reverse('persons:user_create'))
        view = UserCreate.as_view()
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shifts/useraccount_form.html')


    def test_auth(self):
        c = Client()
        response = c.get(reverse('shifts:shift_list'))
        self.assertEquals(response.status_code, 302)
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('shifts:shift_list'))
        self.assertEquals(response.status_code, 200)


    def test_fake_creation(self):
        self.assertEqual(False, True)
