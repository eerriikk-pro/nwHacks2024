import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from geooding.scrape_gmaps import get_photos_by_place_id

# Create your views here.


def load_map(request):
    context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "home.html", context)


def process_place_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        place_id = data.get("placeId")

        photos = get_photos_by_place_id(place_id)

        return JsonResponse({"status": "success", "message": "Place ID processed"})
