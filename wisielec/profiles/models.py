# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=u'Avatar')
    score = models.IntegerField(verbose_name=u"Scores", default=0)
    won_games = models.IntegerField(verbose_name=u"Games (won)", default=0)
    lost_games = models.IntegerField(verbose_name=u"Games (lost)", default=0)
    won_tournaments = models.IntegerField(verbose_name=u"Tournaments (won)", default=0)
    lost_tournaments = models.IntegerField(verbose_name=u"Tournaments (lost)", default=0)
    objects = UserManager()
