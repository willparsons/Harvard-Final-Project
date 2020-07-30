from django.db import models

from users.models import Profile


class Room(models.Model):
    name = models.CharField(max_length=32, unique=True)
    participants = models.ManyToManyField(Profile, related_name="rooms")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}: {self.name}"

    @staticmethod
    def get_room(name: str) -> ('Room', bool):
        return Room.objects.get_or_create(name=name)

    # TODO: All rooms should be private by default, require permission to join
    def add_participant(self, participant):
        # TODO: If the user already exists, it will trigger signals
        self.participants.add(participant)

    def remove_participant(self, participant):
        self.participants.remove(participant)

    def get_messages(self, amt=None):
        if amt is None:
            return self.messages.all().order_by("timestamp")[-10:]

        return self.messages.all().order_by("timestamp")[-amt:]


class Message(models.Model):
    """
    TODO:   perhaps in the future messages will stay even if users are removed,
            but their profile will change to a 'dead' one
    """
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="sent_messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")

    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.room.id}): {self.author.user.username}"
