from django.conf.urls import url
from .views import profile_view, ranking_view, profile_edit_view, guest_login


urlpatterns = [
    url(r'^guest/', guest_login, name='guest_login'),
    url(r'^ranking', ranking_view, name='ranking_view'),
    url(r'^edit/$', profile_edit_view, name='edit_profile'),

    # game stuff
    url(r'^view/(?P<username>.*)/$', profile_view, name='profile_view'),
]
