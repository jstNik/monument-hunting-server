from django.db import models
from django.forms import model_to_dict
from monuments.models import Monument
from zones.models import Zone


# Create your models here.
class Riddle(models.Model):
    body = models.TextField()
    monument = models.ForeignKey(Monument, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)

    def serialize(self):
        d = model_to_dict(self)
        d["monument"] = self.monument.serialize()
        return d

    def __str__(self):
        return self.monument.__str__()
