import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from nwhacks2024.geooding.scrape_gmaps import get_photos_by_place_id
from django.views.decorators.http import require_http_methods

# Create your views here.


def load_map(request):
    context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "home.html", context)


def process_place_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        place_id = data.get("placeId")

        image_urls = get_photos_by_place_id(place_id)

        return render(request, 'image_gallery.html', {'image_urls': image_urls})


@require_http_methods(["POST"])
def process_image(request):
    # Parse the request body to get the data
    data = json.loads(request.body)
    image_url = data.get('imageUrl')

    # Process the image URL as needed
    # ...

    return JsonResponse({'status': 'success', 'message': 'Image processed'})
