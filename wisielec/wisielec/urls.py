from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from profiles.views import profile_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls')),
    url(r'^game/', include("game.urls")),
    url(r'^profiles/', include("profiles.urls")),
    url(r'^$', include("home.urls")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', profile_view, name='your_profile_view'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
