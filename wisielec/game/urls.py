from django.conf.urls import url
from views import new_game, current_game, guess_phrase

urlpatterns = [
    url(r'^new', new_game, name='new_game'),
    url(r'^(?P<session_id>.*)/guess$', guess_phrase, name='guess_phrase'),
    url(r'^(?P<session_id>.*)/$', current_game, name='current_game'),
]
