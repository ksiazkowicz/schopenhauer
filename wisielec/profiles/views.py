from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms import RegistrationForm
from profiles.models import UserProfile


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = UserProfile

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(UserProfile.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('accounts:register-done')


def login_view(request, template="profiles/login_view.html"):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/game/new")
        else:
            error = "Invalid username or password"

    return render(request, template, locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/game/new")


def profile_view(request, username, template='profiles/profile_view.html'):
    user = get_object_or_404(UserProfile, username=username)
    return render(request, template, locals())
