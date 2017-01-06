# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseServerError
from profiles.models import UserProfile
from game.models import Tournament
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.template import Context, Template, loader


def generate_html(request):
    """
    Generates HTML code from request. You should send a JSON through post this way:

    csrfmiddlewaretoken=token&data={"template": "includes/decadence/cancer.html", ...}

    Data should have a template + context.
    """
    # get request data from JSON first
    request_data = request.POST.get("data", "{}")
    # parse as JSON
    request_data = json.loads(request_data)

    # get template file path
    template_file = request_data.get("template", "")

    # check if path is valid
    if not template_file.startswith("includes/decadence/"):
        return HttpResponseServerError("<h1>Invalid template</h1>")

    # load the template
    t = loader.get_template(template_file)
    c = Context(request_data)
    # render and return as response
    rendered = t.render(c)

    return HttpResponse(rendered, content_type="text/html")


@csrf_exempt
def tournament_invite_api(request):
    """
    Invites user to tournament.
    """
    if request.POST:
        tournament = get_object_or_404(Tournament, session_id=request.POST.get("tournament_id"))
        user = get_object_or_404(UserProfile, username=request.POST.get("username"))
        tournament.players.add(user)
        response = {"result": "success", "session_id": tournament.session_id}
    else:
        response = {"result": "fail"}

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_api(request, session_id=None):
    """
    Returns list of tournaments for player.
    """
    if session_id:
        tournaments = Tournament.objects.filter(session_id=session_id)
    else:
        tournaments = request.user.tournament_set.all()

    response = {"tournaments": [{
        "name": t.name,
        "session_id": t.session_id,
        "in_progress": t.in_progress,
        "players": [x.username for x in t.players.all()],
    } for t in tournaments]}

    return HttpResponse(json.dumps(response), content_type="application/json")


def user_api(request, username=None):
    """
    Returns currently logged in player.
    """
    if not username:
        user = request.user
    else:
        user = get_object_or_404(UserProfile, username=username)

    if user.is_authenticated():
        response = {
            "username": user.username,
            "authenticated": user.is_authenticated(),
            "avatar": "",
            "overall_score": user.score,
            "ranking_score": user.ranking_score,
            "position": user.ranking_position,
            "won_games": user.won_games,
            "lost_games": user.lost_games,
            "won_tournaments": user.won_tournaments,
            "lost_tournaments": user.lost_tournaments,
            "tournaments": [x.session_id for x in user.tournament_set.all()],
        }
    else:
        response = {
            "username": "AnonymousUser",
            "authenticated": user.is_authenticated(),
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
