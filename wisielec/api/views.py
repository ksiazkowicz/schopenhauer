# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from profiles.models import UserProfile


def user_api(request):
    """
    Returns currently logged in player.
    """
    if request.user.is_authenticated():
        response = {
            "username": request.user.username,
            "authenticated": request.user.is_authenticated(),
            "avatar": "",
            "overall_score": request.user.score,
            "ranking_score": request.user.ranking_score,
            "position": request.user.ranking_position,
            "won_games": request.user.won_games,
            "lost_games": request.user.lost_games,
            "won_tournaments": request.user.won_tournaments,
            "lost_tournaments": request.user.lost_tournaments,
            "tournaments": [x.session_id for x in request.user.tournament_set.all()],
        }
    else:
        response = {
            "username": "AnonymousUser",
            "authenticated": request.user.is_authenticated(),
            "avatar": "",
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
