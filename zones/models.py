from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import *
import json
from django.forms import model_to_dict


# Create your models here.
class Zone(Model):
    name = CharField(max_length=100)
    coordinates = TextField()
    color = IntegerField(
        default=0,
        validators=[MaxValueValidator(0xFFFFFF), MinValueValidator(0x000000)]
    )

    def transform_coords(self):
        self.coordinates = json.loads(self.coordinates)

    def serialize(self):
        self.transform_coords()
        return model_to_dict(self)

    def __str__(self):
        return self.name
