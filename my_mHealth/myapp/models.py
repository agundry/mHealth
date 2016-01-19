from django.db import models

# Create your models here.
class ProximityReading(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField(default=0)
    message = models.CharField(max_length=30, blank=False)