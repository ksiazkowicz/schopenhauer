from django.conf.urls import url
from views import lobby_view, new_game, current_game

urlpatterns = [
    url(r'^lobby', lobby_view, name='lobby_view'),
    url(r'^new', new_game, name='new_game'),
    url(r'^(?P<session_id>.*)/$', current_game, name='current_game'),
]
