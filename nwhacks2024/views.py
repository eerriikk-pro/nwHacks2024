import json

import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django_datatables_view.base_datatable_view import BaseDatatableView

from nwhacks2024.document_parse.document_parser import extract_table
from nwhacks2024.geooding.scrape_gmaps import get_photos_by_place_id
from nwhacks2024.utils import join_tables

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
            table = extract_table(image_url)
            break
        except:
            continue
    # for table in tables:
    #     print(table.caption)
    #     print(table.dataframe)

    # df = join_tables(tables)
    # file_path = "table.csv"
    # df = pd.read_csv(file_path)
    df = table.dataframe
    print(df)
    # df_combined = (
    #     df.groupby("type")
    #     .apply(lambda x: x.iloc[0].combine_first(x.iloc[1]))
    #     .reset_index()
    # )
    # df_combined.to_csv("table.csv")
    # # print(df.head())
    # print(df_combined)
    # Convert the DataFrame to HTML
    df_html = df.to_html()

    request.session["df_html"] = df_html

    return JsonResponse({"redirect_url": "/menu_filter/"})


from openai import OpenAI


def menu_filter(request):
    # Handle form submission
    if request.method == "POST":
        search_term = request.POST.get("search", "")

    # Retrieve image URLs from session
    df_html = request.session.get("df_html", [])

    # return client.chat.completions.create(
    #     model="gpt-4-vision-preview",
    #     response_model=Table,
    #     max_tokens=1800,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": """Extract data from the table, which is a menu.
    #                                 Table should have a title, description, price, and dietary restrictions column if applicable.
    #                                 If there seem to be multiple tables, add another table column representing the title of the table (label the column type), hence joining all the tables into one.
    #                                 Dietary restrictions may include gluten-free, vegan, vegetarian, kosher, halal, and any other common restrictions.
    #                                 Only include restrictions that are mentioned in the menu (might be a symbol), othewise keep blank""",
    #                 },
    #                 {"type": "image_url", "image_url": {"url": url}},
    #             ],
    #         }
    #     ],
    # )

    # # Clear the session data
    # if "df_html" in request.session:
    #     del request.session["df_html"]

    return render(
        request, "menu_filter.html", {"df_html": df_html, "search_term": search_term}
    )
