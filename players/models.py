from django.contrib.auth.models import AbstractUser
from zones.models import Zone


class Player(AbstractUser):

    def serialize(self):
        d = {
            "id": self.id,
            "username": self.username
        }
        return d
