# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0026_userinfo_admin_type_sigle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Userinfo')),
            ],
        ),
    ]