from .weathercodes import WEATHER_ICON, WEATHER_CLOTHING
from www.models import Settings, Weather


def GetTemperatureStatus(temp_high):
    config = Settings.objects.first()
    temperatures = [
        {"title": "colder", "lowerBound": config.colder},
        {"title": "cold", "lowerBound": config.cold},
        {"title": "fair", "lowerBound": config.fair},
        {"title": "warm", "lowerBound": config.warm}
    ]
    try:
        return [status["title"] for status in temperatures if temp_high > status["lowerBound"]][-1]
    except IndexError:
        return 'cold'


def GetClothingIcon(code, temp_high):
    weather = Weather.objects.get(code=code)
    try:
        status = GetTemperatureStatus(temp_high)
        clothing = getattr(weather, status)
        return clothing.icon
    except (IndexError, AttributeError):
        return 'jacket'


def GetWeatherIcon(code, daytime):
    try:
        return WEATHER_ICON[code]["day" if daytime else "night"]
    except IndexError:
        return 'cloud'

