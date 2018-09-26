from www.models import Settings, Weather
from www.taps.forecast import is_taps_aff, F_TO_C


def GetTemperatureStatus(temp_high_c, weather):
    temperatures = [
        {"title": "colder", "lowerBound": weather.colder},
        {"title": "cold", "lowerBound": weather.cold},
        {"title": "fair", "lowerBound": weather.fair},
        {"title": "warm", "lowerBound": weather.warm}
    ]
    try:
        return [status["title"] for status in temperatures if temp_high_c > status["lowerBound"]][-1]
    except IndexError:
        return 'cold'


def GetClothingIcon(code, temp_high_f):
    weather = Weather.objects.get(code=code)
    try:
        if is_taps_aff(code, temp_high_f):
            return 'tapsaff'

        temp_high_c = F_TO_C(temp_high_f)
        status = GetTemperatureStatus(temp_high_c, weather)
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

