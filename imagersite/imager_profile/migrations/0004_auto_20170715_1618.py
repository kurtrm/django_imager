# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-15 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0003_auto_20170620_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]