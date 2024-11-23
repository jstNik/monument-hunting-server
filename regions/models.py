from django.db import models

class Region(models.Model):
    name = models.CharField(blank=False, null=False)
    coordinates = models.JSONField()
    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "coordinates": self.coordinates,
            "color": self.color
        }