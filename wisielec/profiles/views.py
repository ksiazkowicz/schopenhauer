from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect

from profiles.forms import ProfileForm
from profiles.models import UserProfile

from django.contrib.auth.decorators import login_required


@login_required
def profile_edit_view(request, template="profiles/userprofile_form.html"):
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.POST:
        if form.is_valid():
            form.save()

        return redirect("profile_view", username=request.user.username)

    return render(request, template, locals())


def ranking_view(request, template="profiles/ranking_view.html"):
    users = sorted(UserProfile.objects.all(), key=lambda t: t.ranking_score, reverse=True)
    return render(request, template, locals())


@login_required
def profile_view(request, username=None, template='profiles/profile_view.html'):
    if not username:
        username = request.user.username
    user = get_object_or_404(UserProfile, username=username)
    return render(request, template, locals())
