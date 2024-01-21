class_name = "Uf0tqf loaded"

import re
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from nwhacks2024.geooding.utils import get_higher_quality

wait_time = 3
# Set the path to your webdriver (e.g., chromedriver)
webdriver_path = "/path/to/your/webdriver"

# Set the search query

# Set the Xpath for the search box
searchbox_xpath = """//*[@id="XmI62e"]"""

# Set the ARIA label for the menu button
menu_button_class_name = "ofKBgf"

menu_button_aria_label = "Menu"

# Set the class name for the photos
# photos_class_name = "Uf0tqf loaded"
photos_class_name = "U39Pmb"

# Initialize the webdriver
driver = webdriver.Chrome()

input_element_attribute = "jslog"
input_element_value = "11886"


def get_photos(search_query):
    try:
        # Open Google Maps
        driver.get("https://maps.google.ca")

        # Find the search box and enter the search query
        input_element = driver.find_element(
            By.CSS_SELECTOR, f'input[{input_element_attribute}="{input_element_value}"]'
        )

        # Wait for the page to load (you may need to adjust the wait time)
        time.sleep(wait_time)

        input_element.send_keys(search_query)
        input_element.send_keys(Keys.RETURN)

        # Wait for the menu to appear (you may need to adjust the wait time)
        time.sleep(wait_time)

        # Find and click the menu button
        menu_button = driver.find_element(
            By.XPATH,
            f'//*[@aria-label="{menu_button_aria_label}"][contains(@class, "{menu_button_class_name}")]',
        )
        menu_button.click()

        time.sleep(wait_time)

        # Find all the photos with the specified class name
        photos = driver.find_elements(By.CLASS_NAME, photos_class_name)

        background_images = []

        for idx, photo in enumerate(photos, start=1):
            background_image = photo.value_of_css_property("background-image")
            print(f"Photo {idx} - Background Image: {background_image}")
            background_images.append(background_image)

        # Download the photos (you may need to implement this part based on your specific requirements)

        # Example: Print the image source URLs
        for photo in photos:
            print(photo.get_attribute("src"))

    finally:
        # Close the webdriver
        driver.quit()
    background_images_parsed = []
    for image in background_images:
        # Use a regular expression to extract the URL between the quotes
        start_index = image.find('"') + 1
        end_index = image.rfind('"')

        if start_index != -1 and end_index != -1:
            extracted_url = image[start_index:end_index]
            high_quality = get_higher_quality(extracted_url)
            if high_quality == "s2000/":
                continue
            background_images_parsed.append(high_quality)
    print(background_images_parsed)
    return background_images_parsed


def get_photos_by_place_id(place_id):
    try:
        url = f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={place_id}"
        # Open Google Maps
        driver.get(url)
        background_images = []
        # Wait for the menu to appear (you may need to adjust the wait time)
        time.sleep(wait_time)

        # Find and click the menu button
        menu_button = driver.find_element(
            By.XPATH,
            f'//*[@aria-label="{menu_button_aria_label}"][contains(@class, "{menu_button_class_name}")]',
        )
        menu_button.click()

        time.sleep(wait_time)

        # Find all the photos with the specified class name
        photos = driver.find_elements(By.CLASS_NAME, photos_class_name)

        for idx, photo in enumerate(photos, start=1):
            background_image = photo.value_of_css_property("background-image")
            print(f"Photo {idx} - Background Image: {background_image}")
            background_images.append(background_image)

        # Download the photos (you may need to implement this part based on your specific requirements)

        # Example: Print the image source URLs
        for photo in photos:
            print(photo.get_attribute("src"))

    finally:
        # Close the webdriver
        driver.quit()
    background_images_parsed = []
    for image in background_images:
        # Use a regular expression to extract the URL between the quotes
        start_index = image.find('"') + 1
        end_index = image.rfind('"')

        if start_index != -1 and end_index != -1:
            extracted_url = image[start_index:end_index]
            high_quality = get_higher_quality(extracted_url)
            if high_quality == "s2000/":
                continue
            background_images_parsed.append(high_quality)
    print(background_images_parsed)
    return background_images_parsed


if __name__ == "__main__":
    get_photos_by_place_id(input("Enter place id: "))
