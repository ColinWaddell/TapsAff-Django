from django.db import models

# Create your models here.

class Settings(models.Model):
    location = models.CharField(max_length=100)
    cache_seconds = models.IntegerField()
    threshold = models.FloatField()
    google_id = models.CharField(max_length=20)
    delta = models.FloatField(default=5)


class Weather(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    scots = models.TextField()
    terrible = models.BooleanField()
    night = models.BooleanField(default=False)
    delta = models.FloatField(default=0)