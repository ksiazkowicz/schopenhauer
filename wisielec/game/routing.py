# In routing.py
from channels.routing import route
from game.consumers import ws_message, ws_add, ws_disconnect, ws_guess

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_guess),
    route("websocket.disconnect", ws_disconnect),
]