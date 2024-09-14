# forecast/models.py
from django.db import models

class Reservoir(models.Model):
    reservoir_name = models.CharField(max_length=255)
    basin = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    full_reservoir_level = models.FloatField(null=True, blank=True)
    live_capacity_frl = models.FloatField(null=True, blank=True)
    storage = models.FloatField(null=True, blank=True)
    level = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.reservoir_name



