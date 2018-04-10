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
        # cached = cache.get(show)

        # if not cached:
        map_icons = icons.get_clothing() if show == 'clothing' else icons.get_weather()
        map_data = render(request, 'map/map.svg', {
            'icons': map_icons,
            'width': icons.C_WIDTH,
            'height': icons.C_HEIGHT
        })
        #     cache.set(show, map_data)
        # else:
        #     map_data = cached

        return HttpResponse(map_data, content_type="image/svg+xml")
