from django.shortcuts import render
from django.views import View

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'tapsaff.html', {})
