# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 23:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0003_auto_20161128_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_id', models.IntegerField(verbose_name='This round ID')),
                ('games', models.ManyToManyField(to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Tournament name')),
                ('current_round', models.IntegerField(verbose_name='Current round')),
                ('mode', models.IntegerField(verbose_name='Game mode')),
                ('tournament_mode', models.IntegerField(verbose_name='Tournament mode')),
                ('session_id', models.CharField(max_length=128, verbose_name='Session ID')),
                ('in_progress', models.BooleanField(default=True, verbose_name='Is in progress?')),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Tournament'),
        ),
        migrations.AddField(
            model_name='round',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]