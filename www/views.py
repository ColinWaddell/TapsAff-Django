from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Settings
from .taps import forecast
from .tapmap import icons


CONFIG = lambda: Settings.objects.first()


class Index(View):
    def get(self, request, location=None):

        if not location:
            try:
                location = request.session['location']
            except KeyError:
                location = None

        weather = forecast.query(location, location_default=CONFIG().location)
        request.session['location'] = weather['location']
        return render(request, 'tapsaff.html', {
            "weather": weather,
            "settings": CONFIG
        })
    
    def post(self, request):
        location = request.POST["location"]
        return redirect("www:index", location=location)

class Api(View):
    def get(self, request, location=None):
        
        data = dict()

        if not location:
            data["error"] = "location not supplied"
        else:
            data = forecast.query(location)
        
        if data["place_error"]:
            data = {
                "error": data["place_error"]
            }

        return JsonResponse(data)


class Map(View):
    def get(self, request, show=''):
        cache_key = f"map:{show}"

        def _build_map():
            map_icons = icons.get_clothing() if show == 'clothing' else icons.get_weather()
            return render(request, 'map/map.svg', {
                'icons': map_icons,
                'width': icons.C_WIDTH,
                'height': icons.C_HEIGHT,
            })

        map_data = cache.get_or_set(
            cache_key, _build_map, timeout=settings.CACHE_MAP_TIMEOUT,
        )
        return HttpResponse(map_data, content_type="image/svg+xml")
