# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_registertime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('description', models.CharField(max_length=128, verbose_name='摘要')),
                ('content', models.TextField(verbose_name='正文')),
                ('img', models.ImageField(upload_to='./static/imgs/', verbose_name='图片')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='t',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Tags'),
        ),
    ]