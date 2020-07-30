import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth.models import User

from .models import Room, Message


# TODO: Reorganise this
# TODO: Timestamp formatting
class ChatConsumer(WebsocketConsumer):
    """
    Synchronous consumer for handling chatting events
    Would be better performance to move the functionality to an asynchronous context, but it proved to be
        very difficult and error-prone
    """

    # noinspection PyAttributeOutsideInit
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user: User = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.room: Room = self.get_room(self.room_name)

        self.accept()

    # Leave room group
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # TODO: wrapper method that will abstract this
        if data["command"] == "fetch_messages":
            self.fetch_messages(data)
        elif data["command"] == "new_message":
            self.new_message(data)

    # Send message to room group
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Sends a message to the WebSocket
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def get_room(self, name: str):
        room, _ = Room.get_room(name)
        room.add_participant(self.user.profile)
        print(f"Participants in current room : {room.participants.all()}")

        return room

    def fetch_messages(self, data):
        messages = self.room.get_messages()

        obj = {
            "command": "batch",
            "data": self.messages_to_json(messages)
        }

        # Send message is used here since only the requesting client should get the initial update
        self.send_message(obj)

    def new_message(self, data):
        try:
            message = self.room.messages.create(author=self.user.profile, room=self.room, content=data["data"])
        except Exception as e:
            print(e)
            message = "INTERNAL SERVER FAILURE"

        obj = {
            "command": "single",
            "data": self.message_to_json(message)
        }

        self.send_chat_message(obj)

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def message_to_json(self, message: Message):
        return {
            "id": message.id,
            "author": message.author.user.username,
            "room": self.room.name,
            "content": message.content,
            "timestamp": str(message.timestamp.time())
        }
