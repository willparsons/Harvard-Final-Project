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

    # TODO: All rooms should be private by default. Requires permission to join
    def add_participant(self, participant: Profile):
        # TODO: If the user already exists, it will trigger signals
        self.participants.add(participant)

    def remove_participant(self, participant: Profile):
        self.participants.remove(participant)

    def get_messages(self, amt: int = 0):
        if amt <= 0:
            return self.messages.all().order_by("-timestamp")[:10][::-1]

        return self.messages.all().order_by("-timestamp")[:amt][::-1]

    def delete_message(self, message_id: int, author: Profile):
        # TODO: setup this
        pass


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
        return f"Room {self.room.id}: {self.author.user.username}"
