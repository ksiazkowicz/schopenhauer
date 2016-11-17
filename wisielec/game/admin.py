from django.contrib import admin
from models import Game


class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ["progress", "session_id", "state", "score"]

admin.site.register(Game, GameAdmin)
