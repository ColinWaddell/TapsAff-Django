from .weathercodes import TEMPERATURES, WEATHER_ICON, WEATHER_CLOTHING

def GetTemperatureStatus(temp_high):
    try:
        return [status["title"] for status in TEMPERATURES if temp_high > status["lowerBound"]][-1]
    except IndexError:
        return 'cold'


def GetClothingIcon(code, temp_high):
    try:
        return WEATHER_CLOTHING[code][GetTemperatureStatus(temp_high)]
    except IndexError:
        return 'jacket'


def GetWeatherIcon(code, daytime):
    try:
        return WEATHER_ICON[code]["day" if daytime else "night"]
    except IndexError:
        return 'cloud'

