from django.contrib import admin
from models import Game, Tournament, Round, ChatMessage


class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ["progress", "session_id", "state", "score"]


class TournamentAdmin(admin.ModelAdmin):
    model = Tournament


class RoundAdmin(admin.ModelAdmin):
    model = Round


class ChatMessageAdmin(admin.ModelAdmin):
    model = ChatMessage
    list_display = ["author", "message", "context"]


admin.site.register(Game, GameAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
