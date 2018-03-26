"""Routing for WebSockets"""
from channels.routing import route_class
from .consumers import GameConsumer, LobbyConsumer, TournamentConsumer, \
    ChatConsumer


routing = [
    route_class(LobbyConsumer, path=r"^/lobby"),
    route_class(GameConsumer, path=r"^/game"),
    route_class(TournamentConsumer, path=r"^/tournament"),
    route_class(ChatConsumer, path=r"^/chat"),
]
