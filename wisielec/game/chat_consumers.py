# -*- coding: utf-8 -*-
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from models import ChatMessage
import json
from pytz import utc
import datetime

auto_ban = {}


def check_for_spam(message, author):
    """
    I would have never possibly thought I'd possibly have to implement this. I mean, it's university project... -_-
    :param message:
    :return:
    """
    # check if message is shorther than 3 chars
    if len(message) < 3:
        return True

    # check if author is flooding the chat
    if len(author.chatmessage_set.all()) > 0:
        timedelta = datetime.datetime.now(utc) - author.chatmessage_set.last().timestamp
        min_time = datetime.timedelta(seconds=20)
        if timedelta < min_time:
            # yeah, flooding
            auto_ban[author.username] = auto_ban.get(author.username, 0) + 1

            # ban user if flooded for too long
            if auto_ban.get(author.username, 0) > 20:
                author.allow_chat = False
                author.save()

            return True

    # calculate random bullshit rate
    alphabet = u"aąbcćdeęfghijklłmnńoprsśtuówyzżź"
    bullshit = 0
    for index, i in enumerate(message.lower()):
        print index, i
        if i not in alphabet and index > 0 and message.lower()[index-1] != i:
            bullshit += 1

    # calculate bullshit rate
    bullshit_rate = float(bullshit)/float(len(message))

    if bullshit_rate > 0.5:
        print "bullshit found"
        # wow, so much bullshit
        return True

    # nothing checks out I guess
    return False


@channel_session_user
def chat_receive(message):
    content = None

    for key, value in message.items():
        if key == "text":
            try:
                content = json.loads(value)
            except:
                content = value

    author = message.user
    context = message.channel_session['context']
    content = content.replace("[[ message ]]", "")
    if content != "":
        # ignore requests if user is banned or message is spam
        if author.allow_chat and not check_for_spam(content, author):
            ChatMessage.objects.create(author=author, context=context, message=content)

        # send updated game status to group
        Group("chat-%s" % context).send({
            "text": json.dumps({
                "author": author.username,
                "message": content,
            }),
        })


@channel_session_user_from_http
def chat_connect(message):
    context_id = message.content['path'].strip("/chat/")
    message.channel_session['context'] = context_id
    # Send last 10 messages
    messages = reversed(ChatMessage.objects.filter(context="lobby").order_by("-pk")[:10])
    for chat_message in messages:
        message.reply_channel.send({
            "text": json.dumps({
                "author": chat_message.author.username,
                "message": chat_message.message,
            }),
        })
    Group("chat-%s" % context_id).add(message.reply_channel)


# Connected to websocket.disconnect
@channel_session_user
def chat_disconnect(message):
    context_id = message.channel_session['context']
    Group("chat-%s" % context_id).discard(message.reply_channel)

