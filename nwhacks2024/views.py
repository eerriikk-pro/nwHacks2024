from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json


def load_map(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'home.html', context)


def process_place_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('placeId')

        print(place_id)

        return JsonResponse({'status': 'success', 'message': 'Place ID processed'})