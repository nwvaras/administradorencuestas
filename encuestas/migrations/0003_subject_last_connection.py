# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-05 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0002_auto_20170105_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='last_connection',
            field=models.DateTimeField(null=True),
        ),
    ]
