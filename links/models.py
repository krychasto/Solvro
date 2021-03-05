from django.db import models

# Create your models here.

class Links(models.Model):
    distance = models.IntegerField()
    source = models.CharField(max_length=500)
    target = models.CharField(max_length=500)

class Stops(models.Model):
    stop_id = models.IntegerField()
    stop_name = models.CharField(max_length=500)