from django.http import HttpResponse
from channels.handler import AsgiHandler
from views import guess_phrase
from django.shortcuts import render, get_object_or_404
from models import Game
from channels import Group
import json


# Connected to websocket.connect
def ws_add(message):
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })


def ws_guess(message):
    content = path = None

    for key, value in message.items():
        if key == "path":
            path = value
        elif key == "text":
            try:
                content = json.loads(value)
            except:
                content = value

    if path == "/guess/":
        session_id = content['session_id']
        letter = content['letter']

        game = get_object_or_404(Game, session_id=session_id)

        yes = False

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

        print "O BOZE TO DZIALA DLACZEGO JAK TO WOOOOW"

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