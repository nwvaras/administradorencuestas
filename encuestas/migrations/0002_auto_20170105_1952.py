# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-05 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='end_survey_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='last_sended_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='sended',
            field=models.BooleanField(default=False),
        ),
    ]
