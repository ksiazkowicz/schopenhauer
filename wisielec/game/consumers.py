from django.shortcuts import get_object_or_404
from models import Game
from views import create_game
from channels import Group
from datetime import datetime
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import json


lobby_players = []
game_players = {}


def push_list_current_games(channel):
    games = Game.objects.all()
    channel.send({
        "text": json.dumps({
            "running_games": [x.session_id for x in games if x.state == "IN_PROGRESS"]
        })
    })

    for x in games:
        if x.state == "IN_PROGRESS":
            push_list_current_players_game(x.session_id)


def push_list_current_players():
    Group("lobby").send({
        "text": json.dumps({
            "players": lobby_players
        })
    })


def push_list_current_players_game(game_id):
    game = Game.objects.get(session_id=game_id)

    Group("lobby").send({
        "text": json.dumps({
            "session_id": game_id,
            "players": game_players.get(game_id, [])
        }),
    })
    Group("game-%s" % game_id).send({
        "text": json.dumps({
            "session_id": game_id,
            "player_list_only": True,
            "players": game_players.get(game_id, [])
        })
    })

@channel_session_user_from_http
def lobby_connect(message):
    # add player to lobby
    Group("lobby").add(message.reply_channel)

    # send out a list of running games
    push_list_current_games(message.reply_channel)

    try:
        lobby_players.append(unicode(message.user))
    except:
        pass

    push_list_current_players()


@channel_session_user
def lobby_disconnect(message):
    Group("lobby").discard(message.reply_channel)
    try:
        lobby_players.remove(unicode(message.user))
    except:
        pass

    push_list_current_players()


@http_session_user
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
        game = create_game(message.user)
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
@channel_session_user_from_http
def ws_connect(message):
    game_id = message.content['path'].strip("/game/")
    message.channel_session['game'] = game_id
    Group("game-%s" % game_id).add(message.reply_channel)
    push_game_status("game-%s" % game_id)

    if not game_players.get(game_id):
        game_players[game_id] = [unicode(message.user)]
    else:
        try:
            game_players.get(game_id, []).append(unicode(message.user))
        except:
            pass

    push_list_current_players_game(game_id)


# Connected to websocket.receive
@channel_session_user
@channel_session
def ws_message(message):
    Group("game-%s" % message.channel_session['game']).send({
        "text": "[user] %s" % message.content['text'],
    })


@http_session_user
@channel_session_user
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
    player = game.player

    if player:
        if player != message.user:
            return

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
                    if player:
                        player.score += 1
                    new_progress += game.phrase[index]
                else:
                    new_progress += game.progress[index]

            game.progress = new_progress
            yes = True
        else:
            game.mistakes += 1
            game.used_characters += letter

        game.update_round()
        game.save()

        if len(game.round_set.all()):
            round = game.round_set.all()[0]
            tournament = round.tournament
            if round.winner:
                for game2 in round.games.all():
                    Group("game-%s" % game2.session_id).send({
                        "text": json.dumps({
                           "redirect": True,
                           "tournament": tournament.session_id})
                        })
            else:
                status_updates = []
                for game2 in round.games.all():
                    status_updates += [{
                        "session_id": game2.session_id,
                        "player": game2.player.username,
                        "mistakes": game2.mistakes,
                        "progress": game2.progress_string
                    }, ]
                for game2 in round.games.all():
                    Group("game-%s" % game2.session_id).send({
                        "text": json.dumps({
                            "updates": status_updates})
                    })

        # keep track of won and lost games
        if player:
            if game.state == "FAIL":
                player.lost_games += 1
            elif game.state == "WIN":
                player.won_games += 1
            player.save()

        # send updated game status to group
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
@channel_session
@channel_session_user
def ws_disconnect(message):
    game_id = message.channel_session['game']
    Group("game-%s" % game_id).discard(message.reply_channel)
    try:
        game_players.get(game_id, []).remove(unicode(message.user))
    except:
        pass

    push_list_current_players_game(game_id)
