from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    friends = models.ManyToManyField(to='self', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def friend_count(self):
        return self.friends.count()

    def add_friend(self, other: 'Profile'):
        self.friends.add(other)

    def remove_friend(self, other: 'Profile'):
        self.friends.remove(other)

    def all_friends(self):
        return self.friends.all()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
