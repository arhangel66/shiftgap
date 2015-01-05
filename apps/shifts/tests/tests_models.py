# -*- coding: utf8 -*-
from django.template.loader import render_to_string
from apps.shifts.tests.fake import gen_fake_users, gen_fake_organizations, gen_fake_shifts
from apps.shifts.views import ShiftListing

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from django.test import TestCase, Client, RequestFactory


class OrganizationModelCreationTest(TestCase):
    def test_fake_creation(self):
        orgs = gen_fake_organizations(2)
        self.assertEqual(len(orgs) == 2, True)


class UserModelCreationTest(TestCase):
    def test_fake_creation(self):
        users = gen_fake_users(5, organization_ids='rand')
        self.assertEqual(len(users), 5)


class ShiftsModelCreationTest(TestCase):
    def test_fake_creation(self):
        shifts = gen_fake_shifts(3, gen_fake_users(2))
        self.assertEqual(len(shifts), 3)


class OrganizationModelTest(TestCase):
    def setUp(self):
        self.org1 = gen_fake_organizations(1)[0]
        self.org1_count_users = 3
        self.users_of_org1 = gen_fake_users(count_user=self.org1_count_users, organization_ids=[self.org1.id])

    def test_get_list_of_users(self):
        self.assertEqual(len(self.org1.get_list_of_users()) , self.org1_count_users)


class UserModelTest(TestCase):
    def setUp(self):
        self.org1 = gen_fake_organizations(1)[0]
        self.org2 = gen_fake_organizations(1)[0]
        self.users_of_org1 = gen_fake_users(3, organization_ids=[self.org1.id])
        self.users_of_org2 = gen_fake_users(3, organization_ids=[self.org2.id])
        self.shift_org1 = gen_fake_shifts(1, [self.users_of_org1[0]])
        self.shift_org2 = gen_fake_shifts(1, [self.users_of_org2[0]])

    def test_fake_creation(self):
        users = gen_fake_users(5, organization_ids='rand')
        self.assertEqual(len(users), 5)

    def test_can_update_shift(self):
        user = self.users_of_org1[0]
        self.assertEqual(hasattr(user, 'can_update_shift'), True)
        self.assertEqual(user.can_update_shift(self.shift_org1[0]), True)
        self.assertEqual(user.can_update_shift(self.shift_org2[0]), False)  # User can't update shift from org2

    def test_can_create_shift(self):
        user = self.users_of_org1[0]
        self.assertEqual(hasattr(user, 'can_create_shift'), True)
        self.assertEqual(user.can_create_shift(), True)  # Now any user can create shift

    def test_can_delete_shift(self):
        user = self.users_of_org1[0]
        self.assertEqual(hasattr(user, 'can_delete_shift'), True)
        self.assertEqual(user.can_delete_shift(self.shift_org1[0]), True)
        self.assertEqual(user.can_delete_shift(self.shift_org2[0]), False)  # User can't delete shift from org2

    def test_can_create_this_shift(self):
        user = self.users_of_org1[0]
        self.assertEqual(hasattr(user, 'can_create_this_shift'), True)
        self.assertEqual(user.can_create_this_shift(self.shift_org1[0]), True)
        self.assertEqual(user.can_create_this_shift(self.shift_org2[0]), False)  # User can't create shift for org2
