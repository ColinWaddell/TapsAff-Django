from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .taps import forecast

# Create your views here.
class Index(View):
    def get(self, request, location='Glasgow'):
        weather = forecast.query(location)
        return render(request, 'tapsaff.html', weather)
    
    def post(self, request):
        weather = forecast.query(request.POST["location"])
        return render(request, 'tapsaff.html', weather)
