# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-11 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_achievement'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='allow_chat',
            field=models.BooleanField(default=True, verbose_name='Allow chat'),
        ),
    ]
