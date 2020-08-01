from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    friends = models.ManyToManyField(to='self', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def all_friends(self):
        return self.friends.all()

    def username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_requests")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user.user.username} to {self.to_user.user.username}"

    def accept(self):
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)
        self.delete()

    def reject(self):
        self.delete()
