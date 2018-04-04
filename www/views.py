from django.shortcuts import render
from django.views import View

from .taps import forecast

# Create your views here.
class Index(View):
    def get(self, request, location='Glasgow'):
        weather = forecast.query(location)
        return render(request, 'tapsaff.html', {
            'location': location,
            'weather': str(weather)
        })
