from django.db import models
from users.models import Profile

import uuid


class Room(models.Model):
    display_name = models.CharField(max_length=32, default="Room")
    name = models.CharField(max_length=32, unique=True)

    participants = models.ManyToManyField(Profile, related_name="rooms")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}: {self.name}"

    @staticmethod
    # todo: make sure this is handling rooms properly
    def get_room(name: str) -> ('Room', bool):
        return Room.objects.get(name=name)

    @staticmethod
    def create_room(display_name: str, participants: [] = None):
        name = uuid.uuid4().hex[:32].upper()  # Should create a unique string value every time

        r = Room.objects.create(display_name=display_name, name=name)

        if participants is not None:
            for p in participants:
                r.add_participant(p)

        return r

    # todo: All rooms should be private by default. Requires permission to join
    def add_participant(self, participant: Profile):
        if participant not in self.participants.all():
            self.participants.add(participant)  # If the user already exists, it will trigger signals

    def remove_participant(self, participant: Profile):
        self.participants.remove(participant)

    def get_messages(self, amt: int = 10):
        return self.messages.all().order_by("-timestamp")[:amt][::-1]

    def delete_message(self, message_id: int, author: Profile):
        # todo: Setup delete
        pass


class Message(models.Model):
    """
    todo:   perhaps in the future messages will stay even if users are removed,
            but their profile will change to a 'dead' one
    """
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="sent_messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")

    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room.id}: {self.author.user.username}"
