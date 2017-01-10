from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^user/(?P<username>.*)/achievements$', achievement_api, name='achievement_api'),
    url(r'^user/(?P<username>.*)$', user_api, name='user_api'),
    url(r'^user/', user_api, name='user_api'),
    url(r'^ranking/', ranking_api, name='ranking_api'),

    url(r'^tournament/create/', tournament_create_api, name='tournament_create_api'),
    url(r'^tournament/invite/', tournament_invite_api, name='tournament_invite_api'),
    url(r'^tournament/(?P<session_id>.*)/scoreboard/', tournament_scoreboard_api, name='tournament_scoreboard_api'),
    url(r'^tournament/(?P<session_id>.*)/rounds/$', tournament_rounds_api, name='tournament_rounds_api'),
    url(r'^tournament/(?P<session_id>.*)/end/$', tournament_end_api, name='tournament_end_api'),
    url(r'^tournament/(?P<session_id>.*)/invite/$', tournament_invite_api, name='tournament_invite_api'),
    url(r'^tournament/(?P<session_id>.*)/new_round/$', tournament_new_round_api, name='tournament_new_round_api'),
    url(r'^tournament/(?P<session_id>.*)$', tournament_api, name='tournament_api'),
    url(r'^tournament/', tournament_api, name='tournament_api'),

    url(r'^game/create/', game_create_api, name='game_create_api'),
    url(r'^game/(?P<session_id>.*)/$', game_info_api, name='game_info_api'),

    url(r'^decadence/template/$', generate_html, name='decadence_template'),
]
