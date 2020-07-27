from django.db import models

from users.models import Profile


# TODO: Maybe create rooms
#   These rooms can store a series of messages
#   This way one the room has been removed, we can clear it from our db

class Message(models.Model):
    """
    TODO:   perhaps in the future messages will stay even if users are removed,
            but their profile will change to a 'dead' one
    """
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="received_messages")

    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} -> {self.recipient.user.username}"
