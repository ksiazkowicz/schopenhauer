from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from models import ChatMessage
import json


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
    messages = ChatMessage.objects.filter(context=context_id).order_by("pk")[10:]
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

