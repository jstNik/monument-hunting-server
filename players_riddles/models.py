from django.db.models import *
from django.forms import model_to_dict

from riddles.models import Riddle
from django.contrib.auth.models import User
from players.models import Player


class PlayersRiddles(Model):
    player = ForeignKey(Player, on_delete=CASCADE)
    riddle = ForeignKey(Riddle, on_delete=CASCADE)
    started_at = DateTimeField(auto_now_add=True)
    completed_at = DateTimeField(auto_now=True)
    is_completed = BooleanField(default=False)

    class Meta:
        unique_together = ("player", "riddle")

    def serialize(self):
        d = model_to_dict(self)
        d["player"] = self.player.serialize()
        d["riddle"] = self.riddle.serialize()
        p_id = d["player"]["id"]
        d["player"].clear()
        d["player"]["id"] = p_id
        z_id = d["riddle"]["monument"]["zone"]["id"]
        d["riddle"]["monument"]["zone"].clear()
        d["riddle"]["monument"]["zone"]["id"] = z_id
        return d

    def __str__(self):
        return f"P{self.player_id}-R{self.riddle_id}"