# In routing.py
from channels.routing import route
from channels.routing import include
from .consumers import *
from .tournament_consumers import *
from .chat_consumers import *


game_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_guess),
    route("websocket.disconnect", ws_disconnect),
]

lobby_routing = [
    route("websocket.connect", lobby_connect),
    route("websocket.receive", lobby_receive),
    route("websocket.disconnect", lobby_disconnect),
]

tournament_routing = [
    route("websocket.connect", tournament_connect),
    route("websocket.receive", tournament_receive),
    route("websocket.disconnect", tournament_disconnect),
]

chat_routing = [
    route("websocket.connect", chat_connect),
    route("websocket.receive", chat_receive),
    route("websocket.disconnect", chat_disconnect),
]

routing = [
    include(lobby_routing, path=r"^/lobby"),
    include(game_routing, path=r"^/game"),
    include(tournament_routing, path=r"^/tournament"),
    include(chat_routing, path=r"^/chat"),
]