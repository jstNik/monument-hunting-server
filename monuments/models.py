from django.db.models import *
from django.forms import model_to_dict

from zones.models import Zone


# Create your models here.
class Monument(Model):
    name = CharField(max_length=50, null=False, blank=False)
    latitude = FloatField(null=False)
    longitude = FloatField(null=False)
    zone = ForeignKey(Zone, on_delete=SET_NULL, null=True)

    def serialize(self):
        d = model_to_dict(self)
        d["zone"] = self.zone_id
        return d

    def __str__(self):
        return self.name
