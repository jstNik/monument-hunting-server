from django.db.models import *
from django.forms import model_to_dict

from regions.models import Region


class Zone(Model):
    name = CharField(max_length=100)
    coordinates = JSONField()
    region = ForeignKey(Region, null=True, on_delete=SET_NULL)

    def serialize(self):
        return model_to_dict(self)

    def __str__(self):
        return self.name
