from django.contrib import admin
from models import Game, Tournament, Round


class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ["progress", "session_id", "state", "score"]


class TournamentAdmin(admin.ModelAdmin):
    model = Tournament


class RoundAdmin(admin.ModelAdmin):
    model = Round

admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Tournament, TournamentAdmin)
