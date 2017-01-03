from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms import ProfileForm
from profiles.models import UserProfile

from django.contrib.auth.decorators import login_required


class RegistrationView(CreateView):
    form_class = ProfileForm
    model = UserProfile

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        return redirect('lobby_view')


@login_required
def profile_edit_view(request, template="profiles/userprofile_form.html"):
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.POST:
        if form.is_valid():
            form.save()

        return redirect("profile_view", username=request.user.username)

    return render(request, template, locals())


def login_view(request, template="profiles/login_view.html"):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby_view')
        else:
            error = "Invalid username or password"

    return render(request, template, locals())


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/game/lobby")


def ranking_view(request, template="profiles/ranking_view.html"):
    users = sorted(UserProfile.objects.all(), key=lambda t: t.ranking_score, reverse=True)
    return render(request, template, locals())


@login_required
def profile_view(request, username=None, template='profiles/profile_view.html'):
    if not username:
        username = request.user.username
    user = get_object_or_404(UserProfile, username=username)
    return render(request, template, locals())
