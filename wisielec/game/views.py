# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from game.models import Game, Tournament
from profiles.models import UserProfile
from django.shortcuts import redirect


def lobby_view(request, template="game/lobby.html"):
    return render(request, template, locals())


def new_game(request, template="new_game.html"):
    return render(request, template, locals())


def new_tournament_view(request, template="new_game.html"):
    is_tournament = True
    return render(request, template, locals())


def current_game(request, session_id, template="game/game.html"):
    game = get_object_or_404(Game, session_id=session_id)
    alphabet = u"aąbcćdeęfghijklłmnńoprsśtuówyzżź"
    return render(request, template, locals())


def tournament_invite_view(request, username, template="tournament/invite.html"):
    tournaments = Tournament.objects.filter(in_progress=True)
    user = get_object_or_404(UserProfile, username=username)

    errors = []
    if request.POST:
        tournament = get_object_or_404(Tournament, session_id=request.POST.get("tournament_id"))
        tournament.players.add(user)
        return redirect("tournament_view", tournament.session_id)

    return render(request, template, locals())


def tournament_view(request, session_id, template="tournament/tournament_lobby.html"):
    tournament = get_object_or_404(Tournament, session_id=session_id)
    coop_mode = "cooperation" in tournament.modifiers
    my_games = []
    # make a list of my games
    for x in tournament.round_set.all():
        if coop_mode:
            my_games += list(x.games.all())
        else:
            my_games += list(x.games.filter(player=request.user))

    if request.POST:
        if "end-tournament" in request.POST.keys():
            tournament.in_progress = False

            if tournament.winner:
                winner = tournament.winner
                winner.won_tournaments += 1
                winner.save()
            for player in tournament.players.all():
                if player != tournament.winner:
                    player.lost_tournaments += 1
                    player.save()
            tournament.save()
            return HttpResponseRedirect("/game/t/%s" % tournament.session_id)

    return render(request, template, locals())

