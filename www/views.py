from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from.models import Settings
CONFIG = lambda: Settings.objects.first()

from .taps import forecast
from .tapmap import icons

from django.core.cache import cache


class Index(View):
    def get(self, request, location=None):
        # Resolve requested location or fallback to session/default for keying
        if not location:
            try:
                location = request.session['location']
            except KeyError:
                location = None

        default_loc = CONFIG().location
        cache_key = f"index:{location or default_loc}"
        cached = cache.get(cache_key)

        if cached:
            # Keep session location in sync even on cache hit
            request.session['location'] = (location or default_loc)
            return cached

        # Cache miss: compute weather, render, cache response
        weather = forecast.query(location, location_default=default_loc)
        request.session['location'] = weather['location']
        response = render(request, 'tapsaff.html', {
            "weather": weather,
            "settings": CONFIG
        })
        cache.set(cache_key, response)
        return response

    def post(self, request):
        location = request.POST["location"]
        return redirect("www:index", location=location)


class Api(View):
    def get(self, request, location=None):
        cache_key = f"api:{location or 'none'}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        if not location:
            data = {"error": "location not supplied"}
        else:
            data = forecast.query(location)
            if data.get("place_error"):
                data = {"error": data["place_error"]}

        response = JsonResponse(data)
        cache.set(cache_key, response)
        return response



class Map(View):
    def get(self, request, show=''):
        cache_key = f"map:{show}"
        cached = cache.get(cache_key)

        if not cached:
            map_icons = icons.get_clothing() if show == 'clothing' else icons.get_weather()
            map_data = render(request, 'map/map.svg', {
                'icons': map_icons,
                'width': icons.C_WIDTH,
                'height': icons.C_HEIGHT
            })
            cache.set(cache_key, map_data)
        else:
            map_data = cached

        return HttpResponse(map_data, content_type="image/svg+xml")
