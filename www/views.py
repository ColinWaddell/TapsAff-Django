from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Settings
from .tapmap import icons
from .taps import forecast


class Index(View):
    def get(self, request, location=None):
        # Resolve requested location, falling back to session then default.
        if not location:
            location = request.session.get("location")

        config = Settings.current()
        weather = forecast.query(location, location_default=config.location)
        request.session["location"] = weather["location"]
        return render(request, "tapsaff.html", {
            "weather": weather,
            "settings": config,
        })

    def post(self, request):
        location = request.POST["location"]
        return redirect("www:index", location=location)


class Api(View):
    def get(self, request, location=None):
        if not location:
            return JsonResponse({"error": "location not supplied"})

        data = forecast.query(location)
        if data.get("place_error"):
            return JsonResponse({"error": data["place_error"]})
        return JsonResponse(data)


class Map(View):
    def get(self, request, show=""):
        cache_key = f"map:{show}"

        def _build_map():
            map_icons = icons.get_clothing() if show == "clothing" else icons.get_weather()
            return render(request, "map/map.svg", {
                "icons": map_icons,
                "width": icons.C_WIDTH,
                "height": icons.C_HEIGHT,
            }).content.decode()

        map_data = cache.get_or_set(
            cache_key, _build_map, timeout=settings.CACHE_MAP_TIMEOUT,
        )
        return HttpResponse(map_data, content_type="image/svg+xml")
