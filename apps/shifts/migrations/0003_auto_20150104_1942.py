# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('shifts', '0002_auto_20141228_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name of organization')),
                ('timezone', models.CharField(max_length=100, default='America/Chicago', verbose_name='Timezone of organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True, serialize=False)),
                ('position', models.CharField(max_length=100, blank=True, null=True)),
                ('timezone', models.CharField(max_length=100, default='America/Chicago', verbose_name='Timezone')),
                ('organization', models.ForeignKey(verbose_name='Organization', null=True, blank=True, to='shifts.Organization')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
        migrations.RemoveField(
            model_name='shift',
            name='employee',
        ),
    ]
