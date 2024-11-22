from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import *
import json
from django.forms import model_to_dict

from regions.models import Region


# Create your models here.
class Zone(Model):
    name = CharField(max_length=100)
    coordinates = JSONField()
    region = ForeignKey(Region, null=True, on_delete=SET_NULL)

    def serialize(self):
        return model_to_dict(self)

    def __str__(self):
        return self.name
