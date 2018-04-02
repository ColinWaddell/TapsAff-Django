from django.shortcuts import render
from django.views import View

# Create your views here.
class Index(View):
    def get(self, request, location='Glasgow'):
        return render(request, 'tapsaff.html', {
            'location': location
        })
