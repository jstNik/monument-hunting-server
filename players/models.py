from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey, SET_NULL
from django.forms import model_to_dict

from zones.models import Zone


class Player(AbstractUser):

    def serialize(self):
        d = {
            "id": self.id,
            "username": self.username
        }
        return d
