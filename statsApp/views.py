from django.shortcuts import render
from django.views import View

from .models import *

class StatsView(View):
    def get(self, request):
        return render(request, 'statistikalar.html')