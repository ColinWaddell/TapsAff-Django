from json import loads
from urllib.request import urlopen
from urllib.parse import quote_plus
from requests import get

from www.models import Weather, Settings
from .settings import URL
from .status import AFF, OAN

from django.utils.timezone import datetime
from django.core.cache import cache


F_TO_C = lambda f: (f-32.0) * (5.0 / 9.0)
CONFIG = lambda: Settings.objects.first()


class TapsLocationError(Exception):
    pass


class TapsRequestError(Exception):
    pass


def _build_query(location):
    return URL.replace("LOCATION", quote_plus(location))


def fetchJson(url):
    cache_key = hash(url)
    cached = cache.get(cache_key)
    content = ""
    if not cached:
            response = get(url)
            if(response.ok):
                cache.set(cache_key, response.text)
                content = response.text
            else:
                # Write some proper error handling code here
                print("Error - status code: %s" % response.status_code)
    else:
        # Return the cached content
        content = cached

    return loads(content)


def _grab_forecast_data(location):
    # Grab the forecast
    query_url = _build_query(location.lower())
    forecast = fetchJson(query_url)
    return forecast


def _build_future_forecast(forecast):
    data = [
        {
            "code": int(daycast["code"]),
            "temp_high_f" : float(daycast["high"]),
            "temp_high_c": F_TO_C(float(daycast["high"])),
            "temp_low_f": float(daycast["low"]),
            "temp_low_c": F_TO_C(float(daycast["low"])),
            "taps": _test_taps_aff(daycast["code"], float(daycast["high"]), True),
            "datetime": datetime.strptime(daycast["date"], '%d %b %Y'),
            "description": _get_description(daycast["code"])
        }
        for daycast in forecast
    ]
    return data


def _test_taps_aff(code, temp_f, daytime):
    # test terrible list: oan
    # test if greater than temp: aff
    # test elif close to boundary: oan
    # must be oan
    taps = {
        'status': OAN,
        'message': ""
    }

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
    return {
        "english": weather.description,
        "scots": weather.scots
    }


def _is_daytime(astronomy):
    sunrise = datetime.strptime(astronomy["sunrise"], "%I:%M %p")
    sunset = datetime.strptime(astronomy["sunset"], "%I:%M %p")
    now = datetime.now()

    return sunrise.time() < now.time() and sunset.time() > now.time()

def _build_packet():
    return {
        'temp_f': 0,
        'temp_c': 0,
        'code': -1,
        'taps': {},
        'aff': False,
        'message': "",
        'description': "",
        'datetime': str(datetime.now()),
        'location': None,
        'daytime': "$daytime",
        'place_error': None,
        'forecast': []
    }

def _build_forecast(packet, raw):
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
            packet["code"] = int(forecast["item"]["condition"]["code"])
            packet["temp_f"] = float(forecast["wind"]["chill"])
            packet["temp_c"] = F_TO_C(packet["temp_f"])
            packet["location"] = forecast["location"]["city"]
            packet["description"] = _get_description(packet["code"])
            packet["daytime"] = _is_daytime(forecast["astronomy"])

            # Taps Aff?
            packet["taps"] = _test_taps_aff(packet["code"], packet["temp_f"], packet["daytime"])
            packet["aff"] = packet["taps"]["status"] == AFF

            # Produce a forecast
            packet["forecast"] = _build_future_forecast(forecast["item"]["forecast"])

        except KeyError:
            raise TapsRequestError()

    return packet


def is_taps_aff(code, temp_f, daytime=True):
    return _test_taps_aff(code, temp_f, daytime)


def query(location_request=None, location_default='Glasgow'):

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
    blah = query('glasgow')
    print(blah)
