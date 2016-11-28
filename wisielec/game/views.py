# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from models import Game
import uuid
import random
from wikiquotes import openSearch, queryTitles, getSectionsForPage, getQuotesForSection


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


def create_game(user, inverse_death=False, max_mistakes=5):
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

        return HttpResponseRedirect("%s" % game.session_id)

    return render(request, template, locals())


def current_game(request, session_id, template="game/game.html"):
    game = get_object_or_404(Game, session_id=session_id)
    alphabet = u"aąbcćdeęfghijklłmnoprsśtuówyzżź"

    return render(request, template, locals())
