from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict


class Player(AbstractUser):

    def serialize(self):
        return model_to_dict(self)
