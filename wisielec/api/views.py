# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseServerError
from profiles.models import UserProfile, Achievement
from game.models import Tournament, Game, create_game
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.template import Context, Template, loader
import uuid


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


def tournament_invite_api(request, session_id=None):
    """
    Invites user to tournament.
    """
    if request.POST:
        # extract tournament
        if session_id:
            tournament = get_object_or_404(Tournament, session_id=session_id)
        else:
            tournament = get_object_or_404(Tournament, session_id=request.POST.get("tournament_id"))

        # check permissions
        if request.user != tournament.admin:
            return HttpResponseServerError("<h1>Server Error</h1>")

        # try to get user by username and add to tournament
        user = get_object_or_404(UserProfile, username=request.POST.get("username"))
        tournament.players.add(user)
        response = {"session_id": tournament.session_id, "username": user.username}
    else:
        return HttpResponseServerError("<h1>Invalid template</h1>")

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_rounds_api(request, session_id):
    """
    Returns a list of round for given tournament.
    :param session_id: tournament ID
    :return: json of all rounds and their winners
    """
    # get tournament
    tournament = get_object_or_404(Tournament, session_id=session_id)
    rounds = tournament.round_set.all().order_by("round_id")

    # prepare response
    response = {
        "session_id": session_id,
        "rounds": [{
            "id": x.round_id,
            "winner": x.get_winner(),
            "status": x.status,
            "games": [{
                "session_id": y.session_id,
                "player": y.player.username if y.player else "",
            } for y in x.games.all()],
        } for x in rounds]
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_scoreboard_api(request, session_id):
    """
    Returns the tournament scoreboard.
    :param session_id: tournament ID
    :return: list of players and their scores
    """
    # get tournament
    tournament = get_object_or_404(Tournament, session_id=session_id)
    round_winners = [x.winner for x in tournament.round_set.all()]

    # prepare response
    response = {
        "session_id": session_id,
        "winner": tournament.winner.username if tournament.winner else "",
        "players": [
            {
                "username": x.username,
                "score": round_winners.count(x),
            } for x in tournament.players.all()],
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_end_api(request, session_id):
    """
    Ends the tournament with given ID
    :param session_id: tournament ID
    :return: json containing final result (winner, his points etc.)
    """
    # get tournament
    tournament = get_object_or_404(Tournament, session_id=session_id)

    # check for permissions
    if request.user != tournament.admin:
        return HttpResponseServerError("<h1>Server error</h1>")

    # end the tournament
    tournament.end_tournament()

    # prepare response
    response = {
        "session_id": session_id,
        "winner": tournament.winner.username if tournament.winner else "",
        "rounds": tournament.current_round,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_api(request, session_id=None):
    """
    Returns list of tournaments for player.
    """
    if request.GET.get("all", False):
        tournaments = Tournament.objects.all()
    else:
        if session_id:
            tournaments = Tournament.objects.filter(session_id=session_id)
        else:
            tournaments = request.user.tournament_set.all()

    if request.GET.get("in_progress", False):
        tournaments = tournaments.filter(in_progress=True)

    response = {"tournaments": [{
        "name": t.name,
        "session_id": t.session_id,
        "in_progress": t.in_progress,
        "modes": t.verbose_mode(),
        "players": [x.username for x in t.players.all()],
    } for t in tournaments]}

    return HttpResponse(json.dumps(response), content_type="application/json")


def tournament_create_api(request):
    """
    Creates a tournament with given parameters.
    """
    if request.POST:
        name = request.POST.get("name", "")
        modifiers = request.POST.get("modifiers", "")

        tournament = Tournament.objects.create(session_id=uuid.uuid1().hex, name=name,
                                               modifiers=modifiers, admin=request.user)
        tournament.players.add(request.user)
        response = {
            "session_id": tournament.session_id,
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseServerError("<h1>Server Error</h1>")


def tournament_new_round_api(request, session_id):
    """
    Returns list of tournaments for player.
    """
    tournament = get_object_or_404(Tournament, session_id=session_id)

    # check permissions
    if request.user != tournament.admin:
        return HttpResponseServerError("<h1>Server Error</h1>")

    # create new round
    tournament.create_new_round()

    response = {
        "current_round": tournament.current_round,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def game_create_api(request):
    """
    Creates a game with given parameters
    """
    if request.POST:
        modifiers = request.POST.get("modifiers", "")
        phrase = request.POST.get("phrase", None)
        game = create_game(request.user, modifiers=modifiers, phrase=phrase)
        response = {
            "session_id": game.session_id,
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseServerError("<h1>Server Error</h1>")


def game_info_api(request, session_id):
    """
    Gives info about game
    :param request:
    :param session_id: ID of the game
    :return: JSON with game info
    """
    game = get_object_or_404(Game, session_id=session_id)

    response = {
        "session_id": game.session_id,
        "progress": game.progress,
        "progress_string": game.progress_string,
        "mistakes": game.mistakes,
        "modes": game.verbose_mode(),
        "player": game.player.username if game.player else "",
        "score": game.score,
    }

    # should add info about other games
    if game.round_set.all():
        response["other_games"] = [{
            "mistakes": x.mistakes,
            "progress": x.progress_string,
            "username": x.player.username if x.player else "",
        } for x in game.round_set.all()[0].games.all()]

    return HttpResponse(json.dumps(response), content_type="application/json")


def achievement_api(request, username):
    """
    Returns a list of achievements, count and progress for player.
    """
    user = get_object_or_404(UserProfile, username=username)

    if user.is_authenticated():
        achievements = Achievement.objects.all().order_by("pk")
        unlocked_achievements = [x for x in achievements if x.evaluate(user)]
        # calculate achievement unlock percentage
        try:
            percentage = int(100 * float(len(unlocked_achievements)) / float(len(achievements)))
        except:
            percentage = 0
        response = {
            "achievements": [{
                "pk": x.pk,
                "name": x.name,
                "description": x.description,
                "unlocked": x in unlocked_achievements,
                "icon": x.icon.url if x.icon else "",
            } for x in achievements],
            "progress": percentage,
            "achievement_count": len(achievements),
        }
    else:
        return HttpResponseServerError("<h1>Server Error</h1>")
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
