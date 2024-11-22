from django.db import models
from django.forms import model_to_dict
from monuments.models import Monument
from zones.models import Zone


# Create your models here.
class Riddle(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    monument = models.ForeignKey(Monument, on_delete=models.SET_NULL, null=True)
    # zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)

    def serialize(self):
        d = model_to_dict(self)
        d["monument"] = self.monument.serialize()
        # d["zone"] = self.zone_id
        return d

    def __str__(self):
        return self.monument.__str__()
