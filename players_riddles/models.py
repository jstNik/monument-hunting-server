from django.db.models import *
from django.forms import model_to_dict
from riddles.models import Riddle
from django.contrib.auth.models import User
from players.models import Player


class PlayersRiddles(Model):
    player = ForeignKey(Player, on_delete=CASCADE)
    riddle = ForeignKey(Riddle, on_delete=CASCADE)

    class Meta:
        unique_together = ("player", "riddle")

    def serialize(self):
        d = model_to_dict(self)
        d["player"] = self.player_id
        d["riddle"] = self.riddle_id
        return d

    def __str__(self):
        return f"P{self.player_id}-R{self.riddle_id}"
