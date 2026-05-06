from django.db import models


class Settings(models.Model):
    """App-wide configuration. Enforced singleton: only one row can ever exist.

    save() coerces pk=1 so a second row can never appear, and current()
    creates the row with sensible defaults on first access. The admin
    sees a single row to edit; calling code can rely on
    Settings.current() always returning a populated instance.
    """

    location = models.CharField(max_length=100)
    cache_seconds = models.IntegerField()
    threshold = models.FloatField()
    google_id = models.CharField(max_length=20)
    delta = models.FloatField(default=5)

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"Settings(location={self.location})"

    def save(self, *args, **kwargs):
        # Collapse every save to pk=1. Together with current()'s
        # get_or_create, this guarantees a single row.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def current(cls):
        """Return the singleton row, creating it with defaults if missing."""
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "location": "Glasgow",
                "cache_seconds": 1800,
                "threshold": 70.0,
                "google_id": "",
                "delta": 5.0,
            },
        )
        return obj


class WeatherIcon(models.Model):
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.icon


class ClothingIcon(models.Model):
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.icon


class Weather(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    scots = models.TextField()
    terrible = models.BooleanField()
    delta = models.FloatField(default=0)
    colder = models.FloatField(default=-273.15)
    cold = models.FloatField(default=5)
    fair = models.FloatField(default=13)
    warm = models.FloatField(default=16)
    clothing_colder = models.ForeignKey(ClothingIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="colder")
    clothing_cold = models.ForeignKey(ClothingIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="cold")
    clothing_fair = models.ForeignKey(ClothingIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="fair")
    clothing_warm = models.ForeignKey(ClothingIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="warm")
    weather_day = models.ForeignKey(WeatherIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="weather_day")
    weather_night = models.ForeignKey(WeatherIcon, on_delete=models.CASCADE, blank=True, null=True, related_name="weather_night")
