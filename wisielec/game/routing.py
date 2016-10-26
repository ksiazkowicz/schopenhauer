# In routing.py
from channels.routing import route
from channels.routing import include
from consumers import *


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

routing = [
    # You can use a string import path as the first argument as well.
    include(lobby_routing, path=r"^/lobby"),
    include(game_routing, path=r"^/game"),
]