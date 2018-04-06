from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .taps import forecast


class Index(View):
    def get(self, request, location=None):

        if not location:
            try:
                location = request.session['location']
            except KeyError:
                location = None

        weather = forecast.query(location)
        request.session['location'] = weather['location']
        return render(request, 'tapsaff.html', weather)
    
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
        
        return JsonResponse(data)
