import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth.models import User

from . import utils
from .models import Room, Message


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
        self.run_command(data)

    # Send message to room group
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    # Sends a message to the WebSocket
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Runs the appropriate command
    def run_command(self, data):
        if data["command"] == "fetch_messages":
            self.fetch_messages(data)

        elif data["command"] == "new_message":
            self.new_message(data)

        elif data["command"] == "delete_message":
            self.delete_message(data)

    # Adds the user as a participant and returns the current room
    def get_room(self, name: str):
        room = Room.get_room(name)
        room.add_participant(self.user.profile)
        print(f"Participants in current room : {room.participants.all()}")

        return room

    # Sends N messages to the WebSocket
    def fetch_messages(self, data):
        messages = self.room.get_messages()

        obj = {
            "command": "fetch_messages",
            "data": utils.messages_to_json(messages, self.room)
        }

        # Send message is used here since only the requesting client should get the initial update
        self.send_message(obj)

    # Adds message to DB and tells the room to add it
    def new_message(self, data):
        message = self.room.messages.create(author=self.user.profile, room=self.room, content=data["data"])

        obj = {
            "command": "new_message",
            "data": utils.message_to_json(message, self.room)
        }

        self.send_chat_message(obj)

    # Removes the message from DB and tells the room to remove it
    def delete_message(self, data):
        # TODO: delete message
        pass
