# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0025_remove_userinfo_admin_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='admin_type_sigle',
            field=models.BooleanField(default=False),
        ),
    ]
