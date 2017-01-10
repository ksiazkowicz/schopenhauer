from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json
from signals import *
from models import Tournament
from django.dispatch.dispatcher import receiver


@channel_session
@channel_session_user_from_http
def tournament_receive(message):
    pass


@channel_session
@channel_session_user_from_http
def tournament_connect(message):
    tournament_id = message.content['path'].replace("/tournament/","")
    message.channel_session['tournament'] = tournament_id
    Group("tournament-%s" % tournament_id).add(message.reply_channel)


@channel_session
@channel_session_user
def tournament_disconnect(message):
    try:
        tournament_id = message.channel_session['tournament']
    except:
        tournament_id = message.content['path'].replace("/tournament/", "")
    Group("tournament-%s" % tournament_id).discard(message.reply_channel)


@receiver(new_tournament_round, sender=Tournament)
def push_redirect(sender, instance, **kwargs):
    """
    Redirect everyone on signal.
    """
    game = kwargs.pop("game_id")
    player = kwargs.pop("player")
    Group("tournament-%s" % instance.session_id).send({
        "text": json.dumps({
            "game": game,
            "player": player.username,
            "redirect": True
        })
    })
