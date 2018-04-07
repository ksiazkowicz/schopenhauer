# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from profiles.models import UserProfile


class Command(BaseCommand):
    """
    Removes inactive guest users
    """

    def handle(self, *args, **options):
        guests = UserProfile.objects.filter(guest=True)
        for guest in guests:
            max_date = guest.date_joined + \
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            if max_date < timezone.now():
                guest.delete()
