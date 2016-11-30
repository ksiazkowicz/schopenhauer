from django.conf.urls import url
from views import lobby_view, new_game, current_game, tournament_view, new_tournament_view, tournament_invite_view

urlpatterns = [
    url(r'^lobby', lobby_view, name='lobby_view'),
    url(r'^new_game', new_game, name='new_game_view'),
    url(r'^new_tournament', new_tournament_view, name='new_tournament_view'),
    url(r'^g/(?P<session_id>.*)/$', current_game, name='game_view'),
    url(r'^t/(?P<session_id>.*)/$', tournament_view, name='tournament_view'),
    url(r'^invite/(?P<username>.*)/$', tournament_invite_view, name='tournament_invite'),
]
