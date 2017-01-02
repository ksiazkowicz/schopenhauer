# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from models import Game, Tournament, Round
from profiles.models import UserProfile
import uuid
import random
from wikiquotes import openSearch, queryTitles, getSectionsForPage, getQuotesForSection
from django.shortcuts import redirect
from channels import Group
import json


# ugh, you should totally get that from wikiquotes
fallback_quotes = [
    u"Czy nie wygląda to, jakby istnienie było pomyłką, której skutki ujawniają się stopniowo coraz bardziej?",
    u"Każde pożegnanie ma coś ze śmierci, każde ponowne spotkanie – coś ze zmartwychwstania.",
    u"Na świecie ma się do wyboru tylko samotność albo pospolitość.",
    u"Nieustanne starania obliczone na usunięcie cierpienia nie dają nic poza zmianą jego postaci.",
    u"Prostytutki to ludzkie ofiary złożone na ołtarzu monogamii.",
    u"Suma cierpień przewyższa u człowieka znacznie sumę rozkoszy.",
    u"Zimno mi psychicznie.",
]


def get_quote():
    # I'm so sad while making this "fix" ;-;
    phrase = "a" * 210

    while len(phrase) > 128:
        # get title
        all_titles = ["śmierć", "Artur Schopenhauer", "życie", "nieszczęście", "niepowodzenie"]
        title = all_titles[random.randint(0, len(all_titles) - 1)]

        # search
        search_results = openSearch(title)

        pages = queryTitles(search_results['response'][0])
        if pages['response'] != "":
            sections = getSectionsForPage(pages['response'])
            quotes = getQuotesForSection(pages['response'], sections['response'][0])

            quotes = quotes['response']
            phrase = quotes[random.randint(0, len(quotes) - 1)]
    return phrase


def create_game(user, inverse_death=False, max_mistakes=5, phrase=None):
    if not phrase:
        try:
            phrase = get_quote()
        except:
            phrase = fallback_quotes[random.randint(0, len(fallback_quotes) - 1)]

    game_progress = ""
    for x in phrase:
        if x.isalpha():
            game_progress += "_"
        else:
            game_progress += x

    game = Game.objects.create(session_id=uuid.uuid1().hex, phrase=phrase, progress=game_progress,
                               used_characters="", player=user, inverse_death=inverse_death, max_mistakes=max_mistakes)
    return game


def lobby_view(request, template="game/lobby.html"):
    """
    Lobby view
    """
    if request.user:
        tournaments = request.user.tournament_set.filter(in_progress=True)
    return render(request, template, locals())


def new_game(request, template="game/new.html"):
    if request.POST:
        mode = int(request.POST.get("game_mode", 0))
        game = None

        if mode == 0:
            # Eutanazol selected
            game = create_game(request.user)
        elif mode == 1:
            # Born To Die selected
            game = create_game(request.user, inverse_death=True)
        elif mode == 2:
            # yolo selected
            game = create_game(request.user, max_mistakes=1)

        return HttpResponseRedirect("/game/g/%s" % game.session_id)

    return render(request, template, locals())


def new_tournament_view(request, template="tournament/new.html"):
    if request.POST:
        game_mode = int(request.POST.get("game_mode", 0))
        name = request.POST.get("name", "")

        tournament = Tournament.objects.create(session_id=uuid.uuid1().hex, name=name, mode=game_mode)
        tournament.players.add(request.user)

        return HttpResponseRedirect("/game/t/%s" % tournament.session_id)

    return render(request, template, locals())


def current_game(request, session_id, template="game/game.html"):
    game = get_object_or_404(Game, session_id=session_id)
    alphabet = u"aąbcćdeęfghijklłmnoprsśtuówyzżź"

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
    rounds = tournament.round_set.all().order_by("round_id")

    if request.POST:
        if "name" in request.POST.keys():
            try:
                user = UserProfile.objects.get(username=request.POST.get("name", ""))
                tournament.players.add(user)
            except:
                pass
        elif "new-round" in request.POST.keys():
                inverse_death = False
                max_mistakes = 5
                if tournament.mode == 1:
                    # Born To Die selected
                    inverse_death = True
                elif tournament.mode == 2:
                    # yolo selected
                    max_mistakes = 1
                try:
                    phrase = get_quote()
                except:
                    phrase = fallback_quotes[random.randint(0, len(fallback_quotes) - 1)]
                round = Round.objects.create(round_id=tournament.current_round+1, tournament=tournament)
                tournament.current_round = tournament.current_round+1
                tournament.save()
                no_mans_game = False
                for player in tournament.players.all():
                    game = create_game(player, phrase=phrase, inverse_death=inverse_death, max_mistakes=max_mistakes)
                    round.games.add(game)
                    if player == request.user:
                        no_mans_game = game

                    Group("tournament-%s" % tournament.session_id).send({
                        "text": json.dumps({
                            "game": game.session_id,
                            "player": game.player.username,
                            "redirect": True
                        })
                    })
                return HttpResponseRedirect("/game/g/%s" % no_mans_game.session_id)
        elif "end-tournament" in request.POST.keys():
            tournament.in_progress = False
            tournament.save()
            return HttpResponseRedirect("/game/t/%s" % tournament.session_id)

    return render(request, template, locals())

