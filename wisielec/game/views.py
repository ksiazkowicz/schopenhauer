# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from models import Game
import uuid


def new_game(request, template="game/new.html"):
    # TODO: get that from wikiquotes in randomized fashion
    phrase = u"Czy nie wygląda to, jakby istnienie było pomyłką, której skutki ujawniają się stopniowo coraz bardziej?"
    game_progress = ""
    for x in phrase:
        if x.isalpha():
            game_progress += "_"
        else:
            game_progress += x

    if request.POST:
        game = Game.objects.create(session_id=uuid.uuid1().hex, phrase=phrase, progress=game_progress,
                                   used_characters="")
        return HttpResponseRedirect("%s" % game.session_id)

    return render(request, template, locals())


def current_game(request, session_id, template="game/game.html"):
    game = get_object_or_404(Game, session_id=session_id)
    alphabet = u"aąbcćdeęfghijklłmnoprstuówyzżź"

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
