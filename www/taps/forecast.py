from urllib.request import urlopen
from urllib.parse import quote_plus
from urllib.error import HTTPError
from requests import get

from www.models import Weather, Settings
from .status import AFF, OAN
from .weathercom import get_weather

from django.utils.timezone import datetime
from django.core.cache import cache
from django.conf import settings


F_TO_C = lambda f: (f - 32.0) * (5.0 / 9.0)
CONFIG = lambda: Settings.objects.first()


class TapsLocationError(Exception):
    pass


class TapsRequestError(Exception):
    pass


def _grab_forecast_data(location):
    # Grab the forecast
    try:
        cache_key = f"forecast:{location}"
        cached = cache.get(cache_key)
        if not cached:
            forecast = get_weather(location, settings.WEATHER_API_ID)
            cache.set(cache_key, forecast)
        else:
            forecast = cached
        return forecast
    except HTTPError:
        raise TapsLocationError


def _build_future_forecast(forecast):
    data = [
        {
            "code": int(daycast["day"]["condition"]["code"]),
            "temp_high_f": float(daycast["day"]["maxtemp_f"]),
            "temp_high_c": float(daycast["day"]["maxtemp_c"]),
            "temp_low_f": float(daycast["day"]["maxtemp_f"]),
            "temp_low_c": float(daycast["day"]["maxtemp_c"]),
            "taps": _test_taps_aff(
                int(daycast["day"]["condition"]["code"]),
                float(daycast["day"]["maxtemp_f"]),
                True,
            ),
            "datetime": datetime.strptime(daycast["date"], "%Y-%m-%d"),
            "description": _get_description(daycast["day"]["condition"]["code"]),
        }
        for daycast in forecast
    ]

    return data


def _test_taps_aff(code, temp_f, daytime):
    # test terrible list: oan
    # test if greater than temp: aff
    # test elif close to boundary: oan
    # must be oan
    taps = {"status": OAN, "message": ""}

    if not Weather.objects.filter(code=code, terrible=True) and daytime:
        delta = Weather.objects.get(code=code).delta
        theshold = CONFIG().threshold + delta
        if temp_f >= theshold:
            taps["status"] = AFF

        elif temp_f + CONFIG().delta > theshold:
            taps["message"] = "...but only by a bawhair!"

    return taps


def _get_description(code):
    weather = Weather.objects.get(code=int(code))
    return {"english": weather.description, "scots": weather.scots}


def _build_packet():
    return {
        "temp_f": 0,
        "temp_c": 0,
        "code": -1,
        "taps": {},
        "aff": False,
        "message": "",
        "description": "",
        "datetime": str(datetime.now()),
        "location": None,
        "daytime": "$daytime",
        "place_error": None,
        "forecast": [],
    }


def _build_forecast(packet, raw):
    # Test if we've got a valid location
    try:
        if not raw["location"] or not raw["current"]:
            raise TapsLocationError()
    except KeyError:
        raise TapsRequestError("Bad data returned from weather service.")

    else:
        # Grab the proper data
        try:
            forecast = raw["current"]
            location = raw["location"]["name"]

            # Stats
            packet["code"] = int(forecast["condition"]["code"])
            packet["temp_f"] = float(forecast["feelslike_f"])
            packet["temp_c"] = F_TO_C(packet["temp_f"])
            packet["location"] = location
            packet["description"] = _get_description(packet["code"])
            packet["daytime"] = int(forecast["is_day"]) == 1

            # Taps Aff?
            packet["taps"] = _test_taps_aff(
                packet["code"], packet["temp_f"], packet["daytime"]
            )
            packet["aff"] = packet["taps"]["status"] == AFF

            # Produce a forecast
            packet["forecast"] = _build_future_forecast(raw["forecast"]["forecastday"])

        except KeyError:
            raise TapsRequestError("Cannot interpret weather data")

    return packet


def is_taps_aff(code, temp_f, daytime=True):
    status = _test_taps_aff(code, temp_f, daytime)
    return not status["status"] == OAN


def query(location_request=None, location_default="Glasgow"):

    # This is where we'll fill up our response
    packet = _build_packet()

    if location_request:
        try:
            forecast_raw = _grab_forecast_data(location_request)
            packet = _build_forecast(packet, forecast_raw)
            return packet

        except TapsLocationError:
            packet["place_error"] = "Location '%s' unknown" % location_request

    # Either there was a search error
    # or no location was supplied
    forecast_raw = _grab_forecast_data(location_default)
    packet = _build_forecast(packet, forecast_raw)
    return packet


if __name__ == "__main__":
    blah = query("glasgow")
    print(blah)
