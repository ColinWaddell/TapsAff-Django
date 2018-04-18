from django.db import models

# Create your models here.

class Settings(models.Model):
    location = models.CharField(max_length=100)
    cache_seconds = models.IntegerField()
    threshold = models.FloatField()
    google_id = models.CharField(max_length=20)
    delta = models.FloatField(default=5)
    colder = models.FloatField(default=-273.15)
    cold = models.FloatField(default=5)
    fair = models.FloatField(default=13)
    warm = models.FloatField(default=16)


class Clothing(models.Model):
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.icon


class Weather(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    scots = models.TextField()
    terrible = models.BooleanField()
    night = models.BooleanField(default=False)
    delta = models.FloatField(default=0)
    colder = models.ForeignKey(Clothing, on_delete=models.CASCADE, blank=True, null=True, related_name="colder")
    cold = models.ForeignKey(Clothing, on_delete=models.CASCADE, blank=True, null=True, related_name="cold")
    fair = models.ForeignKey(Clothing, on_delete=models.CASCADE, blank=True, null=True, related_name="fair")
    warm = models.ForeignKey(Clothing, on_delete=models.CASCADE, blank=True, null=True, related_name="warm")
    