from django.shortcuts import render
from django.conf import settings


def load_map(request):
    return render(request, 'home.html')