from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)

    # if connection type is websocket, go to AuthMiddlewareStack
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # this tells it where to find our consumers
            chat.routing.websocket_urlpatterns
        )
    ),
})
