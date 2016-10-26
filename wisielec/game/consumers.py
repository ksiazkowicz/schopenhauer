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


# Connected to websocket.connect
"""
@channel_session
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
"""


def ws_connect(message):
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })


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
            yes = True
        else:
            game.mistakes += 1
            game.used_characters += letter

        game.save()

        Group("chat").send({
            "text": json.dumps({
                "mistakes": game.mistakes,
                "session_id": session_id,
                "progress": game.progress,
                "letter": letter,
                "score": game.score,
                "outcome": yes,
            }),
        })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)