from django.contrib import admin
from .models import Settings, Weather, Clothing


class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'description',
        'scots',
        'terrible',
        'delta',
        'night',
        'colder',
        'cold',
        'fair',
        'warm'
    )

    ordering = (
        'code',
    )


class ClothingAdmin(admin.ModelAdmin):
    list_display = (
        'icon',
    )


admin.site.register(Settings)
admin.site.register(Clothing, ClothingAdmin)
admin.site.register(Weather, WeatherAdmin)
