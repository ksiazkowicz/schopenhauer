from __future__ import unicode_literals

from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'

    def ready(self):
        import game.signals.handlers  # noqa
