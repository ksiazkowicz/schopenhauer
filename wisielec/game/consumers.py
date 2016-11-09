from django.shortcuts import get_object_or_404
from models import Game
from views import create_game

from channels import Group
from datetime import datetime
from channels.sessions import channel_session

import json


def push_list_current_games(channel):
    games = Game.objects.all()
    channel.send({
        "text": json.dumps({
            "running_games": [x.session_id for x in games if x.state == "IN_PROGRESS"]
        })
    })


# TODO: actually be able to tell players apart
def lobby_connect(message):
    # add player to lobby
    Group("lobby").add(message.reply_channel)

    # send out a list of running games
    push_list_current_games(message.reply_channel)


# ugh i cant into websockets
def lobby_disconnect(message):
    Group("lobby").discard(message.reply_channel)


def lobby_receive(message):
    content = None

    for key, value in message.items():
        if key == "text":
            try:
                content = json.loads(value)
            except:
                content = value

    action = content['action']
    if action == "new":
        game = create_game()
        session_id = game.session_id
        Group("lobby").send({
            "text": json.dumps({
                "new": True,
                "mistakes": game.mistakes,
                "session_id": session_id,
                "progress": game.progress,
                "score": game.score,
                "used_chars": game.used_characters,
            }),
        })


def push_game_status(channel):
    session_id = channel.strip("game-")
    game = Game.objects.get(session_id=session_id)
    Group(channel).send({
        "text": json.dumps({
            "mistakes": game.mistakes,
            "session_id": session_id,
            "progress": game.progress,
            "score": game.score,
            "used_chars": game.used_characters,
        }),
    })


@channel_session
def ws_connect(message):
    game_id = message.content['path'].strip("/game/")
    message.channel_session['game'] = game_id
    Group("game-%s" % game_id).add(message.reply_channel)
    push_game_status("game-%s" % game_id)


# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group("game-%s" % message.channel_session['game']).send({
        "text": "[user] %s" % message.content['text'],
    })

@channel_session
def ws_guess(message):
    content = None

    for key, value in message.items():
        if key == "text":
            try:
                content = json.loads(value)
            except:
                content = value

    session_id = content['session_id']
    letter = content['letter']

    game = get_object_or_404(Game, session_id=session_id)

    yes = False

    if game.state == "IN_PROGRESS":
        if letter in game.used_characters:
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
            yes = True
        else:
            game.mistakes += 1
            game.used_characters += letter

        game.save()

        Group("game-%s" % message.channel_session['game']).send({
            "text": json.dumps({
                "mistakes": game.mistakes,
                "session_id": session_id,
                "progress": game.progress,
                "letter": letter,
                "score": game.score,
                "outcome": yes,
                "state": game.state,
            }),
        })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)