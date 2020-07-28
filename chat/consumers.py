import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import redirect

from .models import Room, Message


# TODO: if user is not authenticated, they should be redirected
class ChatConsumer(AsyncWebsocketConsumer):
    # noinspection PyAttributeOutsideInit
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user: User = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.room: Room = await self.get_room(self.room_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        await self.save_message(message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_room(self, name: str):
        room, _ = Room.get_room(name)
        room.add_participant(self.user.profile)
        print(room.participants.all())

        return room

    @database_sync_to_async
    def save_message(self, content):
        try:
            self.room.messages.create(author=self.user.profile, room=self.room, content=content)
        except Exception as e:
            print(e)
