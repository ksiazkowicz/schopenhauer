from django.conf.urls import url
from home.views import homepage_view

urlpatterns = [
    url(r'^$', homepage_view, name='home'),
]