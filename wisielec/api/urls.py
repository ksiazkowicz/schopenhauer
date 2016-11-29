from django.conf.urls import url
from views import user_api, ranking_api

urlpatterns = [
    url(r'^user', user_api, name='user_api'),
    url(r'^ranking', ranking_api, name='ranking_api'),
]
