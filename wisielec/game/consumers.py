"""WebSocket consumers"""
# -*- coding: utf-8 -*-
import json
import datetime
from pytz import utc
from django.shortcuts import get_object_or_404
from channels import Group
from channels.generic.websockets import WebsocketConsumer


from .models import Game, ChatMessage


LOBBY_PLAYERS = []
GAME_PLAYERS = {}
AUTO_BAN = {}


def check_for_spam(author):
    """
    I would have never possibly thought I'd possibly have to implement this.
    I mean, it's university project... -_-
    :param message:
    :return:
    """
    # check if user should be allowed to see the chat first
    if not author.allow_chat:
        return True

    # check if author is flooding the chat
    if author.chatmessage_set.all().count() > 0:
        timedelta = datetime.datetime.now(
            utc) - author.chatmessage_set.last().timestamp
        min_time = datetime.timedelta(microseconds=500000)
        if timedelta < min_time:
            # yeah, flooding
            AUTO_BAN[author.username] = AUTO_BAN.get(author.username, 0) + 1

            # ban user if flooded for too long
            if AUTO_BAN.get(author.username, 0) > 20:
                author.allow_chat = False
                author.save()

            return True

    # nothing checks out I guess
    return False


# pylint: disable=redefined-builtin
class ChatConsumer(WebsocketConsumer):
    """
    Chat Consumer
    """
    http_user = True

    def connect(self, message, **kwargs):
        if not message.user.allow_chat:
            message.reply_channel.send({'close': True})
            return
        message.reply_channel.send({'accept': True})

        context_id = message.content['path'][len("/chat/"):]
        message.channel_session['context'] = context_id
        # Send last 10 messages
        # TODO: prerender this
        messages = reversed(ChatMessage.objects.filter(
            context=context_id).order_by("-pk")[:10])
        for chat_message in messages:
            message.reply_channel.send({
                "text": json.dumps({
                    "author": chat_message.author.username,
                    "message": chat_message.message,
                }),
            })
        Group("chat-%s" % context_id).add(message.reply_channel)

    def receive(self, text=None, bytes=None, **kwargs):
        author = self.message.user
        context = self.message.channel_session['context']
        text = json.loads(text).get("message", "")
        text = text.replace("[[ message ]]", "")
        if text != "":
            # ignore requests if user is banned or message is spam
            if check_for_spam(author):
                return

            ChatMessage.objects.create(
                author=author, context=context, message=text)

            # send message
            Group("chat-%s" % context).send({
                "text": json.dumps({
                    "author": author.username,
                    "message": text,
                }),
            })

    def disconnect(self, message, **kwargs):
        context_id = message.channel_session['context']
        Group("chat-%s" % context_id).discard(message.reply_channel)


class TournamentConsumer(WebsocketConsumer):
    """
    Tournament Consumer
    """
    http_user = True

    def connect(self, message, **kwargs):
        tournament_id = message.content['path'].replace("/tournament/", "")
        message.channel_session['tournament'] = tournament_id
        Group("tournament-%s" % tournament_id).add(message.reply_channel)
        message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        try:
            tournament_id = message.channel_session['tournament']
        except KeyError:
            tournament_id = message.content['path'].replace("/tournament/", "")
        Group("tournament-%s" % tournament_id).discard(message.reply_channel)


class LobbyConsumer(WebsocketConsumer):
    """
    Lobby Consumer
    """
    http_user = True

    @staticmethod
    def update_player_list():
        """Helper method for keeping player list updated"""
        Group("lobby").send({
            "text": json.dumps({
                "players": LOBBY_PLAYERS
            })
        })

    def connect(self, message, **kwargs):
        # add player to lobby
        Group("lobby").add(message.reply_channel)
        message.reply_channel.send({'accept': True})

        # send out a list of running games
        # TODO: prerender this
        games = Game.objects.filter(player=message.user)
        message.reply_channel.send({
            "text": json.dumps({
                "running_games": [{
                    "session_id": x.session_id,
                    "progress": x.progress,
                } for x in games if x.state == "IN_PROGRESS" and not
                    x.round_set.count()]
            })
        })

        username = message.user.username
        if username not in LOBBY_PLAYERS:
            LOBBY_PLAYERS.append(username)
        LobbyConsumer.update_player_list()

    def receive(self, text=None, bytes=None, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        Group("lobby").discard(message.reply_channel)
        if message.user.username in LOBBY_PLAYERS:
            LOBBY_PLAYERS.remove(str(message.user))
        LobbyConsumer.update_player_list()


class GameConsumer(WebsocketConsumer):
    """
    Game consumer
    """
    http_user = True

    @staticmethod
    def update_player_list(game_id):
        """Helper method, updates list of players in a game"""
        Group("game-%s" % game_id).send({
            "text": json.dumps({
                "session_id": game_id,
                "player_list_only": True,
                "players": GAME_PLAYERS.get(game_id, [])
            })
        })

    def connect(self, message, **kwargs):
        game_id = message.content['path'][len("/game/"):]
        game = Game.objects.get(session_id=game_id)
        message.channel_session['game'] = game_id
        message.reply_channel.send({'accept': True})
        Group("game-%s" % game_id).add(message.reply_channel)
        Group("game-%s" % game_id).send({
            "text": json.dumps({
                "mistakes": game.mistakes,
                "session_id": game_id,
                "progress": game.progress,
                "progress_string": game.progress_string,
                "score": game.score,
                "used_chars": game.used_characters,
            }),
        })
        GAME_PLAYERS.setdefault(game_id, []).append(message.user.username)
        GameConsumer.update_player_list(game_id)

    def receive(self, text=None, bytes=None, **kwargs):
        content = json.loads(text)

        session_id = content['session_id']
        letter = content['letter'][:1]

        # get the game and attempt to guess a letter
        game = get_object_or_404(Game, session_id=session_id)
        outcome = game.guess(self.message.user, letter)

        # push round status too
        if game.round_set.all().count():
            # get game winner
            this_round = game.round_set.first()

            # let all clients know that the round in tournament has finished
            # prepare status update
            status_updates = []
            for game in this_round.games.all():
                player = game.player
                status_updates.append({
                    "session_id": game.session_id,
                    "player": player.username if player else "Wszyscy",
                    "mistakes": game.mistakes,
                    "progress": game.progress_string
                })

            # push status update to all players
            for game in this_round.games.all():
                Group("game-%s" % game.session_id).send({
                    "text": json.dumps({"updates": status_updates})
                })

            # if round ended, send redirect packet
            if this_round.status != "ROUND_IN_PROGRESS":
                for game in this_round.games.all():
                    winner = this_round.winner
                    Group("game-%s" % game.session_id).send({
                        "text": json.dumps({
                            "tournament": this_round.tournament.session_id,
                            "winner": winner.username if winner else "",
                            "round": this_round.round_id,
                            "redirect": True,
                        })
                    })

        # send updated game status to group
        Group("game-%s" % self.message.channel_session['game']).send({
            "text": json.dumps({
                "mistakes": game.mistakes,
                "hangman_pic": game.get_mistake_count,
                "session_id": session_id,
                "progress": game.progress,
                "progress_string": game.progress_string,
                "letter": letter,
                "score": game.score,
                "outcome": outcome,
                "state": game.state,
            }),
        })

    def disconnect(self, message, **kwargs):
        game_id = message.channel_session['game']
        Group("game-%s" % game_id).discard(message.reply_channel)
        try:
            GAME_PLAYERS.setdefault(game_id, []).remove(message.user.username)
        except ValueError:
            pass
        GameConsumer.update_player_list(game_id)
