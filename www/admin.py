from django.contrib import admin
from .models import Settings, Weather


class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'description',
        'scots',
        'terrible',
        'delta',
        'night',
    )

    ordering = (
        'code',
    )

admin.site.register(Settings)
admin.site.register(Weather, WeatherAdmin)
