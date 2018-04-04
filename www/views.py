from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .taps import forecast

# Create your views here.
class Index(View):
    def get(self, request, location='Glasgow'):
        weather = forecast.query(location)
        return render(request, 'tapsaff.html', weather)
    
    def post(self, request):
        location = request.POST["location"]
        return redirect("www:index", location=location)
