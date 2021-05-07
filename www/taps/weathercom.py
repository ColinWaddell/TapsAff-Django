import urllib.request, json


def build_url(location, api_key):
    return (
        "http://api.weatherapi.com/v1/forecast.json?"
        f"key={api_key}&"
        f"q={location}&"
        "days=3&"
        "aqi=no&"
        "alerts=no"
    )


def get_weather(location, api_key):
    data = None
    with urllib.request.urlopen(build_url(location, api_key)) as url:
        data = json.loads(url.read().decode())

    return data
