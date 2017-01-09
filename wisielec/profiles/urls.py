from django.conf.urls import url
from views import profile_view, ranking_view, profile_edit_view


urlpatterns = [
    url(r'^ranking', ranking_view, name='ranking_view'),
    url(r'^edit/$', profile_edit_view, name='edit_profile'),

    # game stuff
    url(r'^view/(?P<username>.*)/$', profile_view, name='profile_view'),
]
