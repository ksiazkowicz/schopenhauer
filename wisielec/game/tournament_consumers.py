import json

from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session
@channel_session_user_from_http
def tournament_receive(message):
    pass


@channel_session
@channel_session_user_from_http
def tournament_connect(message):
    tournament_id = message.content['path'].replace("/tournament/", "")
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
