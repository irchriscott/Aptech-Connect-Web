# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptechapp', '0006_auto_20190329_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='languages',
            field=models.TextField(default='English', max_length=255),
        ),
    ]