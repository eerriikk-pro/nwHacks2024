import json
import os

import pandas as pd
import requests

GEOCODING_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def find_placeid(place, api_key=GEOCODING_API_KEY):
    base_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.photos,places.formattedAddress",
    }

    data = {"textQuery": place}
    json_data = json.dumps(data)
    response = requests.post(base_url, data=json_data, headers=headers)
    if response.status_code == 200:
        places_data = response.json().get("places", [])
        df = pd.json_normalize(places_data)

        # Extract photo information
        photo_list = []
        for index, row in df.iterrows():
            place_name = row["displayName.text"]
            photos = row.get("photos", [])
            for photo in photos:
                photo_info = {
                    "place_name": place_name,
                    "photo_name": photo["name"],
                    "width_px": photo["widthPx"],
                    "height_px": photo["heightPx"],
                    "author_display_name": photo["authorAttributions"][0][
                        "displayName"
                    ],
                    "author_uri": photo["authorAttributions"][0]["uri"],
                    "photo_uri": photo["authorAttributions"][0]["photoUri"],
                }
                photo_list.append(photo_info)

        # Create a DataFrame for the photos
        photo_df = pd.DataFrame(photo_list)

        # Print the DataFrames
        print("Places DataFrame:")
        print(df)
        print("\nPhotos DataFrame:")
        print(photo_df)
        # df.to_csv("places.csv", index=False)
        # photo_df.to_csv("photos.csv", index=False)

    else:
        print(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


if __name__ == "__main__":
    place = input("Enter a place: ")
    find_placeid(place)
