# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0029_auto_20161227_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favor',
            name='click_count',
        ),
        migrations.RemoveField(
            model_name='favor',
            name='ctime',
        ),
    ]
