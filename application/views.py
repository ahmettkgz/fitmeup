from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, "index.html")
