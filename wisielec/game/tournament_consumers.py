from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json

tournament_players = {}


def push_list_current_players_tournament(game_id):
    """game = Game.objects.get(session_id=game_id)

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
    })"""
    pass


@channel_session
@channel_session_user_from_http
def tournament_receive(message):
    pass


@channel_session
@channel_session_user_from_http
def tournament_connect(message):
    tournament_id = message.content['path'].strip("/tournament/")
    message.channel_session['tournament'] = tournament_id
    Group("tournament-%s" % tournament_id).add(message.reply_channel)
    push_list_current_players_tournament(tournament_id)


# Connected to websocket.disconnect
@channel_session
@channel_session_user
def tournament_disconnect(message):
    tournament_id = message.channel_session['tournament']
    Group("tournament-%s" % tournament_id).discard(message.reply_channel)
    try:
        tournament_players.get(tournament_id, []).remove(unicode(message.user))
    except:
        pass

    push_list_current_players_tournament(tournament_id)
