# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('status', models.BooleanField()),
                ('authcode', models.CharField(max_length=32)),
            ],
        ),
    ]
