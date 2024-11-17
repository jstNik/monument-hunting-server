from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey, SET_NULL
from django.forms import model_to_dict

from zones.models import Zone


class Player(AbstractUser):
    zone = ForeignKey(Zone, null=True, on_delete=SET_NULL)

    def serialize(self):
        d = {
            "id": self.id,
            "username": self.username,
            "zone": self.zone_id
        }
        return d
