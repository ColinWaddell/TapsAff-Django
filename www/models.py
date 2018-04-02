from django.db import models

# Create your models here.

class Settings(models.Model):
    location = models.TextField()
    cache_seconds = models.IntegerField()
    threshold = models.FloatField()


class Weather(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    scots = models.TextField()
    terrible = models.BooleanField()
    night = models.BooleanField(default=False)