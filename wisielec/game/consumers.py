from django.shortcuts import get_object_or_404
from models import Game, Tournament
from channels import Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import json


lobby_players = []
game_players = {}


def push_list_current_games(channel):
    games = Game.objects.all()
    channel.send({
        "text": json.dumps({
            "running_games": [x.session_id for x in games if x.state == "IN_PROGRESS" and x.round_set.count() == 0]
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
    try:
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
    except:
        pass

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
    """if action == "new":
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
        })"""


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


def push_round_status(round):
    """
    Updates status of given round.
    """
    # prepare status update
    status_updates = []
    for game in round.games.all():
        status_updates += [{
            "session_id": game.session_id,
            "player": game.player.username if game.player else "Wszyscy",
            "mistakes": game.mistakes,
            "progress": game.progress_string
        }, ]

    # push status update to all players
    for game in round.games.all():
        Group("game-%s" % game.session_id).send({
            "text": json.dumps({
                "updates": status_updates})
        })

    # if round ended, send redirect packet
    if round.status != "ROUND_IN_PROGRESS":
        for game in round.games.all():
            Group("game-%s" % game.session_id).send({
                "text": json.dumps({
                    "tournament": round.tournament.session_id,
                    "winner": round.winner.username if round.winner else "",
                    "round": round.round_id,
                    "redirect": True,
                })
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
    letter = content['letter'][:1]

    # get the game and attempt to guess a letter
    game = get_object_or_404(Game, session_id=session_id)
    outcome = game.guess(message.user, letter)

    # push round status too
    if len(game.round_set.all()):
        # get game winner
        this_round = game.round_set.all()[0]

        # push a message to all clients that the round in tournament has finished
        push_round_status(this_round)

    # send updated game status to group
    Group("game-%s" % message.channel_session['game']).send({
        "text": json.dumps({
            "mistakes": game.mistakes,
            "hangman_pic": game.get_mistake_count,
            "session_id": session_id,
            "progress": game.progress,
            "letter": letter,
            "score": game.score,
            "outcome": outcome,
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
