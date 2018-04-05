from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .taps import forecast

# Create your views here.
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
