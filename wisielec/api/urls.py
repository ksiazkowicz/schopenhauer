from django.conf.urls import url
from views import user_api, ranking_api, tournament_api, tournament_invite_api

urlpatterns = [
    url(r'^user/(?P<username>.*)$', user_api, name='user_api'),
    url(r'^user/', user_api, name='user_api'),
    url(r'^ranking/', ranking_api, name='ranking_api'),
    url(r'^tournament/invite/', tournament_invite_api, name='tournament_invite_api'),
    url(r'^tournament/(?P<session_id>.*)$', tournament_api, name='tournament_api'),
    url(r'^tournament/', tournament_api, name='tournament_api'),
]
