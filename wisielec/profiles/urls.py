from django.conf.urls import url
from views import login_view, logout_view, profile_view, RegistrationView, ranking_view, profile_edit_view
from django.contrib.auth import views

urlpatterns = [
    url(r'^login', login_view, name='login_view'),
    url(r'^logout', logout_view, name='logout_view'),
    url(r'^ranking', ranking_view, name='ranking_view'),

    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^edit/$', profile_edit_view, name='edit_profile'),
    url(r'^register/done/$', views.password_reset_done, {
        'template_name': 'registration/initial_done.html',
    }, name='register-done'),

    url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, {
        'template_name': 'registration/initial_confirm.html',
        'post_reset_redirect': 'accounts:register-complete',
    }, name='register-confirm'),
    url(r'^register/complete/$', views.password_reset_complete, {
        'template_name': 'registration/initial_complete.html',
    }, name='register-complete'),

    # game stuff
    url(r'^view/(?P<username>.*)/$', profile_view, name='profile_view'),
]
