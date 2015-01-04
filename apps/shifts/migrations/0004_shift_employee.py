# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0003_auto_20150104_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='employee',
            field=models.ForeignKey(default=None, verbose_name='UserAccount', to='shifts.UserAccount'),
            preserve_default=False,
        ),
    ]
