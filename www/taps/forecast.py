from json import loads
from urllib.request import urlopen
from urllib.parse import quote_plus
from settings import URL
from status import AFF, OAN

from datetime import datetime, time


F_TO_C = lambda f: (f-32.0) * (5.0 / 9.0)


class TapsLocationError(Exception):
    pass


class TapsRequestError(Exception):
    pass


def _build_query(location):
    return URL.replace("LOCATION", quote_plus(location))


def _grab_forecast(location):
    # Grab the forecast
    query_url = _build_query(location)
    url = urlopen(query_url)
    forecast = loads(url.read().decode())
    return forecast


def _test_taps_aff(code, temp_f):
    # test terrible list: oan
    # test if greater than temp: aff
    # test elif close to boundary: oan
    # must be oan
    return {
        'status': AFF if temp_f > 62 else OAN,
        'message': "hello"
    }


def _get_description(code):
    return "blah"


def _is_daytime(astronomy):
    sunrise = datetime.strptime(astronomy["sunrise"], "%I:%M %p")
    sunset = datetime.strptime(astronomy["sunset"], "%I:%M %p")
    now = datetime.now()

    return sunrise.time() < now.time() and sunset.time() > now.time()


def _decode_forecast(raw):
    # The packet we need to return
    weather = {
        'temp_f': "$temp_f",
        'temp_c': "$temp_c",
        'code': "$weather_code",
        'taps': "$taps_status['status']",
        'message': "$taps_status['message']",
        'description': "$weather_description",
        'datetime': "$current_datetime->format('Y-m-d H:i:s')",
        'location': "$location",
        'daytime': "$daytime",
        'place_error': "(isset($place_error) ? $place_error : '')",
        'forecast': "$forecast"
    }

    # Test if we've got a valid location
    try:
        if raw["query"]["count"] == 0:
            raise TapsLocationError()
    except KeyError:
        raise TapsRequestError()

    # Grab the proper data
    try:
        try:
            forecast = raw["query"]["results"]["channel"][0]
        except KeyError:
            forecast = raw["query"]["results"]["channel"]
            
        weather["temp_f"] = int(forecast["wind"]["chill"])
        weather["temp_c"] = F_TO_C(weather["temp_f"])
        weather["location"] = forecast["location"]["city"]
        weather["code"] = int(forecast["item"]["condition"]["code"])
        weather["description"] = _get_description(weather["code"])
        weather["daytime"] = _is_daytime(forecast["astronomy"])
        weather["taps"] = _test_taps_aff(weather["temp_f"], weather["code"])
        # Produce a forecast

    except KeyError:
        raise TapsRequestError()

    return weather


def query(location):
    # Grab the weather
    forecast_raw = _grab_forecast(location)
    forecast = _decode_forecast(forecast_raw)

    # Grab the weather
    return forecast

if __name__ == "__main__":
    blah = query('glasgow')
    print(blah)