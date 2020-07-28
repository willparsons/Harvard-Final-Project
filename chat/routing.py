from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # /chat/<str>/ <- will call ChatConsumer
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
