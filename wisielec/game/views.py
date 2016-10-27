# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from models import Game
import uuid
import random
import requests


# ugh, you should totally get that from wikiquotes
quotes = [
    u"Czy nie wygląda to, jakby istnienie było pomyłką, której skutki ujawniają się stopniowo coraz bardziej?",
    u"Każde pożegnanie ma coś ze śmierci, każde ponowne spotkanie – coś ze zmartwychwstania.",
    u"Na świecie ma się do wyboru tylko samotność albo pospolitość.",
    u"Nieustanne starania obliczone na usunięcie cierpienia nie dają nic poza zmianą jego postaci.",
    u"Prostytutki to ludzkie ofiary złożone na ołtarzu monogamii.",
    u"Suma cierpień przewyższa u człowieka znacznie sumę rozkoszy.",
    u"Zimno mi psychicznie.",
]


def create_game(phrase):
    # TODO: get that from wikiquotes in randomized fashion
    game_progress = ""
    for x in phrase:
        if x.isalpha():
            game_progress += "_"
        else:
            game_progress += x

    game = Game.objects.create(session_id=uuid.uuid1().hex, phrase=phrase, progress=game_progress,
                               used_characters="")
    return game


def new_game(request, template="game/lobby.html"):
    if request.POST:
        try:
            quote = request.POST["quote"]
        except:
            quote = quotes[random.randint(0, len(quotes) - 1)]
        game = create_game(quote)
        return HttpResponseRedirect("%s" % game.session_id)

    return render(request, template, locals())


def current_game(request, session_id, template="game/game.html"):
    game = get_object_or_404(Game, session_id=session_id)
    alphabet = u"aąbcćdeęfghijklłmnoprsśtuówyzżź"

    return render(request, template, locals())


def guess_phrase(request, session_id):
    game = get_object_or_404(Game, session_id=session_id)
    letter = request.GET.get("letter", "")

    if letter in game.used_characters:
        print "ugh"
        game.mistakes += 1
    elif letter in game.phrase.lower():
        game.used_characters += letter
        new_progress = ""

        for index, org_letter in enumerate(game.phrase.lower()):
            if letter == org_letter:
                game.score += 1
                new_progress += game.phrase[index]
            else:
                new_progress += game.progress[index]

        game.progress = new_progress
    else:
        game.mistakes += 1
        game.used_characters += letter

    game.save()

    return HttpResponseRedirect("/game/%s" % session_id)
