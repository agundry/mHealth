# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-18 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_deviceuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='beaconreading',
            name='status',
            field=models.CharField(default='', max_length=10),
        ),
    ]
