from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^game/', include("game.urls")),
    url(r'^profiles/', include("profiles.urls")),
    url(r'^/', include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
