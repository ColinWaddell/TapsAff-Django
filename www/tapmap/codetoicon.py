from www.models import Settings, Weather


def GetTemperatureStatus(temp_high, weather):
    temperatures = [
        {"title": "colder", "lowerBound": weather.colder},
        {"title": "cold", "lowerBound": weather.cold},
        {"title": "fair", "lowerBound": weather.fair},
        {"title": "warm", "lowerBound": weather.warm}
    ]
    try:
        return [status["title"] for status in temperatures if temp_high > status["lowerBound"]][-1]
    except IndexError:
        return 'cold'


def GetClothingIcon(code, temp_high):
    weather = Weather.objects.get(code=code)
    try:
        status = GetTemperatureStatus(temp_high, weather)
        clothing = getattr(weather, "clothing_" + status)
        return clothing.icon
    except (IndexError, AttributeError):
        return 'jacket'


def GetWeatherIcon(code, daytime):
    try:
        weather = Weather.objects.get(code=code)
        return weather.weather_day.icon if daytime else weather.weather_night.icon
    except IndexError:
        return 'cloud'

