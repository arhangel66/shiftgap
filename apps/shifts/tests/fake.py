# -*- coding: utf8 -*-
from random import choice, randint
import datetime

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from apps.shifts.models import Shift, UserAccount, Organization
from faker import Factory


fake = Factory.create('en')
fen = Factory.create()


def gen_fake_organizations(count_organizations=3):
    """
    gen fake organizations with fake
    :param count_organizations:
    :return:
    """
    organization_list = []
    for i in range(count_organizations):
        params = {
            'name': fake.company(),
            'timezone': fake.timezone(),
        }
        organization_list.append(Organization.objects.create(**params))

    return organization_list

def gen_fake_users(count_user=20, organization_ids=None, timezone='', email='', name=''):
    """
    :param count_user:
    :return:
    """
    if not organization_ids:
        organization_ids = []
    if organization_ids == 'rand':
        organization_ids = list(Organization.objects.all().values_list('id', flat=True))

    list_user_dicts = []
    for i in range(count_user):
        params = {
            'first_name': fake.name().split(' ')[0] if not name else name,
            'last_name': fake.name().split(' ')[1] if not name else name,
            'username': fake.user_name(),
            'organization_id': choice(organization_ids) if organization_ids else None,
            'password': fake.password(),
            'email': fen.email() if not email else email,
            'timezone': fake.timezone() if not timezone else timezone,
        }
        # print(params)
        user = UserAccount.objects.create_user(**params)
        list_user_dicts.append(user)
        # print(user, user.first_name, user.timezone, user.organization.name)

    return list_user_dicts


def gen_fake_shifts(count_shifts, users = [], start=None, end=None):
    shift_list = []
    from pytz import timezone
    import pytz
    if users:
        for i in range(count_shifts):
            start_time = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(days=randint(1, 7), hours=randint(-2, 5)) if not start else start

            params = {
                'start_time': start_time,
                'end_time':  start_time + datetime.timedelta(hours=randint(1, 8)) if not end else end,
                'employee': choice(users)
            }
            # print(params)
            shift = Shift.objects.create(**params)
            shift_list.append(shift)

    return shift_list