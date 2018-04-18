from django.contrib import admin
from .models import Settings, Weather, ClothingIcon, WeatherIcon


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
        'warm',
        'clothing_colder',
        'clothing_cold',
        'clothing_fair',
        'clothing_warm',
        'weather_day',
        'weather_night',
    )

    ordering = (
        'code',
    )


class ClothingIconAdmin(admin.ModelAdmin):
    list_display = (
        'icon',
    )


class WeatherIconAdmin(admin.ModelAdmin):
    list_display = (
        'icon',
    )


admin.site.register(Settings)
admin.site.register(ClothingIcon, ClothingIconAdmin)
admin.site.register(WeatherIcon, WeatherIconAdmin)
admin.site.register(Weather, WeatherAdmin)
