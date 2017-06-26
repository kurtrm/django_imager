# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0005_auto_20170626_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='photo',
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(default='', related_name='albums', to='imager_images.Photo'),
        ),
    ]
