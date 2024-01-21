import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from nwhacks2024.geooding.scrape_gmaps import get_photos_by_place_id
from django.views.decorators.http import require_http_methods

from nwhacks2024.document_parse.document_parser import extract_table
from nwhacks2024.geooding.scrape_gmaps import get_photos_by_place_id

# Create your views here.


def load_map(request):
    context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "home.html", context)


def process_place_id(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            place_id = data.get("placeId")

            # Use Selenium to gather menu images
            image_urls = get_photos_by_place_id(place_id)

            # Store image URLs in session
            request.session["image_urls"] = image_urls

            return JsonResponse({"redirect_url": "/menu_gallery/"})
        except Exception as e:
            # Log the exception for debugging
            print(f"Error: {e}")
            # Return a JSON response with the error message
            return JsonResponse({"error": str(e)}, status=500)


def menu_gallery(request):
    # Retrieve image URLs from session
    image_urls = request.session.get("image_urls", [])

    # Clear the session data
    if "image_urls" in request.session:
        del request.session["image_urls"]

    return render(request, "image_gallery.html", {"image_urls": image_urls})


@require_http_methods(["POST"])
def process_image(request):
    # Parse the request body to get the data
    data = json.loads(request.body)
    image_url = data.get("imageUrl")
    print(image_url)
    count = 0
    while True:
        try:
            count = count + 1
            if count > 5:
                break
            print(count)
            tables = extract_table(image_url)
            break
        except:
            continue
    for table in tables:
        print(table.caption)
        print(table.dataframe)

    # Process the image URL as needed
    # ...

    return JsonResponse({"status": "success", "message": "Image processed"})
