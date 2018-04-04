from json import loads
from urllib.request import urlopen
from urllib.parse import quote_plus

from www.models import Weather, Settings
from .settings import URL
from .status import AFF, OAN

from django.utils.timezone import datetime


F_TO_C = lambda f: (f-32.0) * (5.0 / 9.0)
CONFIG = lambda: Settings.objects.first()


class TapsLocationError(Exception):
    pass


class TapsRequestError(Exception):
    pass


def _build_query(location):
    return URL.replace("LOCATION", quote_plus(location))


def _grab_forecast_data(location):
    # Grab the forecast
    query_url = _build_query(location)
    url = urlopen(query_url)
    forecast = loads(url.read().decode())
    return forecast


def _build_future_forecast(forecast):
    data = [
        {
            "code": int(daycast["code"]),
            "temp_high_f" : float(daycast["high"]),
            "temp_high_c": F_TO_C(float(daycast["high"])),
            "temp_low_f_": float(daycast["low"]),
            "temp_low_f": F_TO_C(float(daycast["low"])),
            "taps": _test_taps_aff(daycast["code"], float(daycast["high"])),
            "datetime": str(daycast["date"])
        }
        for daycast in forecast
    ]
    return data


def _test_taps_aff(code, temp_f):
    # test terrible list: oan
    # test if greater than temp: aff
    # test elif close to boundary: oan
    # must be oan
    taps = {
        'status': OAN,
        'message': ""
    }

    if not Weather.objects.filter(code=code, terrible=True).count:
        theshold = CONFIG.threshold
        if temp_f > theshold:
            taps["status"] = AFF
        elif temp_f + 5 > theshold:
            taps["message"] = "...but only by a bawhair!"
    
    return taps


def _get_description(code):
    weather = Weather.objects.get(code=int(code))
    return {
        "english": weather.description,
        "scots": weather.scots
    }


def _is_daytime(astronomy):
    sunrise = datetime.strptime(astronomy["sunrise"], "%I:%M %p")
    sunset = datetime.strptime(astronomy["sunset"], "%I:%M %p")
    now = datetime.now()

    return sunrise.time() < now.time() and sunset.time() > now.time()


def _decode_forecast(raw, default_location="Glasgow"):
    # The packet we need to return
    weather = {
        'temp_f': 0,
        'temp_c': 0,
        'code': -1,
        'taps': {},
        'aff': False,
        'message': "$taps_status['message']",
        'description': "",
        'datetime': str(datetime.now()),
        'location': default_location,
        'daytime': "$daytime",
        'place_error': None,
        'forecast': []
    }

    # Test if we've got a valid location
    try:
        if raw["query"]["count"] == 0:
            raise TapsLocationError()
    except KeyError:
        raise TapsRequestError()
    else:
        # Grab the proper data
        try:
            try:
                forecast = raw["query"]["results"]["channel"][0]
            except KeyError:
                forecast = raw["query"]["results"]["channel"]
                
            # Stats
            weather["code"] = int(forecast["item"]["condition"]["code"])
            weather["temp_f"] = float(forecast["wind"]["chill"])
            weather["temp_c"] = F_TO_C(weather["temp_f"])
            weather["location"] = forecast["location"]["city"]
            weather["description"] = _get_description(weather["code"])
            weather["daytime"] = _is_daytime(forecast["astronomy"])

            # Taps Aff?
            weather["taps"] = _test_taps_aff(weather["temp_f"], weather["code"])
            weather["aff"] = weather["taps"]["status"] == AFF

            # Produce a forecast
            weather["forecast"] = _build_future_forecast(forecast["item"]["forecast"])
        except KeyError:
            raise TapsRequestError()

    return weather


def query(location):
    # Grab the weather
    forecast_raw = _grab_forecast_data(location)
    forecast = _decode_forecast(forecast_raw)

    # Need to try a location
    # and if a place error
    # occurs then retry with
    # a cookie or default
    # to Glasgow

    # Grab the weather
    return forecast

if __name__ == "__main__":
    blah = query('glasgow')
    print(blah)