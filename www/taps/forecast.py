from urllib.error import HTTPError

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import datetime

from www.models import Settings, Weather

from .status import AFF, OAN
from .weathercom import get_weather


F_TO_C = lambda f: (f - 32.0) * (5.0 / 9.0)


class TapsLocationError(Exception):
    pass


class TapsRequestError(Exception):
    pass


def _grab_forecast_data(location):
    """Fetch a forecast for `location`, caching by location name.

    TTL is taken from the singleton Settings row's `cache_seconds` field
    so it can be tuned at runtime via the admin without a redeploy. If
    no Settings row exists yet (fresh install) the cache uses the
    backend's default timeout.
    """
    cache_key = f"forecast:{location}"
    config = Settings.current()
    timeout = config.cache_seconds if config else None
    try:
        return cache.get_or_set(
            cache_key,
            lambda: get_weather(location, settings.WEATHER_API_ID),
            timeout=timeout,
        )
    except HTTPError:
        raise TapsLocationError


def _build_daily_forecast(forecast):
    data = [
        {
            "code": int(daycast["day"]["condition"]["code"]),
            "temp_high_f": float(daycast["day"]["maxtemp_f"]),
            "temp_high_c": float(daycast["day"]["maxtemp_c"]),
            "temp_low_f": float(daycast["day"]["mintemp_f"]),
            "temp_low_c": float(daycast["day"]["mintemp_c"]),
            "taps": _test_taps_aff(
                int(daycast["day"]["condition"]["code"]),
                float(daycast["day"]["maxtemp_f"]),
                True,
            ),
            "datetime": datetime.strptime(daycast["date"], "%Y-%m-%d"),
            "description": _get_description(daycast["day"]["condition"]["code"]),
            "hourly": [
                {
                    "hour": hour,
                    "temp_f": float(hourcast["temp_f"]),
                    "temp_c": float(hourcast["temp_c"]),
                    "code": int(hourcast["condition"]["code"]),
                    "taps": _test_taps_aff(
                        int(hourcast["condition"]["code"]),
                        float(hourcast["temp_f"]),
                        True,
                    ),
                    "description": _get_description(hourcast["condition"]["code"]),
                    "precip_mm": float(hourcast["precip_mm"]),
                    "will_it_rain": hourcast["will_it_rain"],
                    "chance_of_rain": hourcast["chance_of_rain"],
                    "will_it_snow": hourcast["will_it_snow"],
                    "chance_of_snow": hourcast["chance_of_snow"],
                }
                for hour, hourcast in enumerate(daycast["hour"])
            ],
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
        config = Settings.current()
        try:
            delta = Weather.objects.get(code=code).delta
        except ObjectDoesNotExist:
            # Unknown weather code — treat as neutral (no delta adjustment)
            delta = 0
        threshold = config.threshold + delta
        if temp_f >= threshold:
            taps["status"] = AFF
        elif temp_f + config.delta > threshold:
            taps["message"] = "...but only by a bawhair!"

    return taps


def _get_description(code):
    try:
        weather = Weather.objects.get(code=int(code))
        return {"english": weather.description, "scots": weather.scots}
    except ObjectDoesNotExist:
        return {"english": "Unknown", "scots": "Unkent"}


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
            packet["forecast"] = _build_daily_forecast(raw["forecast"]["forecastday"])

        except KeyError:
            raise TapsRequestError("Cannot interpret weather data")

    return packet


def is_taps_aff(code, temp_f, daytime=True):
    status = _test_taps_aff(code, temp_f, daytime)
    return not status["status"] == OAN


def query(location_request=None, location_default="Glasgow"):
    """Look up the weather for `location_request`, falling back to
    `location_default` if missing or unknown. Always returns a packet -
    if both lookups fail, the packet's `place_error` field is set so
    callers can render a graceful message instead of getting a 500.
    """
    packet = _build_packet()

    if location_request:
        try:
            forecast_raw = _grab_forecast_data(location_request)
            return _build_forecast(packet, forecast_raw)
        except TapsLocationError:
            packet["place_error"] = f"Location '{location_request}' unknown"

    # Fall back to the default. If that ALSO fails (API down, expired
    # key, malformed response), surface it via place_error rather than
    # bubbling up as a 500.
    try:
        forecast_raw = _grab_forecast_data(location_default)
        return _build_forecast(packet, forecast_raw)
    except (TapsLocationError, TapsRequestError) as exc:
        if not packet["place_error"]:
            packet["place_error"] = f"Forecast unavailable: {exc}"
        return packet
