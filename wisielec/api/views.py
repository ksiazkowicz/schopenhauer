# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from profiles.models import UserProfile


def user_api(request):
    """
    Returns currently logged in player.
    """
    response = {
        "username": request.user,
        "authenticated": request.user.is_authenticated,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def ranking_api(request):
    """
    Returns list of players and their scores.
    """
    users = sorted(UserProfile.objects.all(), key=lambda t: t.ranking_score, reverse=True)

    response = { "players": [{
        "position": index+1,
        "username": user.username,
        "score": user.ranking_score,
    } for index, user in enumerate(users)]}

    return HttpResponse(json.dumps(response), content_type="application/json")
