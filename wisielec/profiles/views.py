# -*- coding: utf-8 -*-
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from profiles.forms import ProfileForm
from profiles.models import UserProfile, Achievement


RANDOM_USERNAMES = [
    [
        "Wielki", "Tani", "Szybki", "Niebezpieczny", "Niezwykły",
        "Zachwycający", "Wyjątkowy", "Nieznośny", "Rakotwórczy",
        "Śmierdzący", "Smakowity", "Seryjny", "Notoryczny", "Obleśny",
        "Tęczowy", "Mroczny",
    ], [
        "Jeździec", "Wisielec", "Chleb", "Rak", "Dekadent", "Samobójca",
        "Wariat", "Ryzykant", "Pesymista", "Zombie", "Obrońca", "Psychofan",
        "Hejter", "Przegryw", "Psychopata", "Wymiatacz", "Wojownik",
    ], [
        "Śmierci", "Apokalipsy", "Krojony", "Mózgu", "", "Szatana",
        "Życia", "Wyprodukowany w Chinach", "Hegla", "Schopenhauera",
        "Przegrywu", "Freuda", "Płaskiej Ziemii", "Lewoskrętnej Witaminy C"
    ],
]


def guest_login(request):
    """Logs in as guest and returns to previous page"""
    if not request.user.is_authenticated() and request.method == "POST":
        # generate random username
        exists = True
        while exists:
            username = " ".join(
                filter(None, [random.choice(x) for x in RANDOM_USERNAMES]))
            exists = UserProfile.objects.filter(username=username)

        # create a new user and log in
        guest = UserProfile.objects.create_user(
            "", "", username=username, guest=True)
        login(request, guest,
              backend='django.contrib.auth.backends.ModelBackend')

    # redirect to previous page
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_edit_view(request, template="account/edit.html"):
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.POST:
        if form.is_valid():
            form.save()

        return redirect("profile_view", username=request.user.username)

    return render(request, template, locals())


def ranking_view(request, template="account/ranking.html"):
    """Shows a sorted list of users"""
    return render(request, template, {
        "users": UserProfile.objects.get_ranking()
    })


@login_required
def profile_view(request, username=None, template='account/view.html'):
    """
    Shows profile view.
    """
    # check if username is provided, if not, use current user
    if not username:
        username = request.user.username
    user = get_object_or_404(UserProfile, username=username)

    # get a list of achievements
    achievements = Achievement.objects.all().order_by('pk')
    unlocked_achievements = []

    # iterate through all of them and evaluate
    for achievement in achievements:
        if achievement.evaluate(user):
            # unlocked, add to list
            unlocked_achievements += [achievement, ]

    # calculate achievement unlock percentage
    try:
        percentage = int(100 * float(len(unlocked_achievements)
                                     ) / float(len(achievements)))
    except ZeroDivisionError:
        percentage = 0

    # render view
    return render(request, template, {
        "percentage": percentage,
        "achievements": achievements,
        "unlocked_achievements": unlocked_achievements,
        "username": username
    })
