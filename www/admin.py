from django.contrib import admin
from .models import Settings, Weather, ClothingIcon


class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'description',
        'scots',
        'terrible',
        'delta',
        'nighttime',
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
admin.site.register(ClothingIcon, ClothingAdmin)
admin.site.register(Weather, WeatherAdmin)
