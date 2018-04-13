"""Game App urls"""
from django.conf.urls import url
from .views import lobby_view, new_game, current_game, tournament_view, \
    tournament_invite_view

urlpatterns = [
    url(r'^$', lobby_view, name='lobby_view'),
    url(r'^game/new/tournament', new_game, {"is_tournament": True},
        name='new_tournament_view'),
    url(r'^game/new', new_game, name='new_game_view'),
    url(r'^game/g/(?P<session_id>.*)/$', current_game, name='game_view'),
    url(r'^game/t/(?P<session_id>.*)/$', tournament_view, name='tournament_view'),
    url(r'^game/invite/(?P<username>.*)/$',
        tournament_invite_view, name='tournament_invite'),
]
