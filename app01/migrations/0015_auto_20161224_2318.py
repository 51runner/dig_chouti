# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 15:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_auto_20161224_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='registered_time',
            field=models.CharField(default=datetime.datetime.now, max_length=64),
        ),
    ]
