# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-24 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_auto_20161224_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='registered_time',
            field=models.DateTimeField(default=0),
        ),
    ]
