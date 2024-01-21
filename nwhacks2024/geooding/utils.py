def get_higher_quality(url):
    start_index = url.find("=") + 1
    end_index = url.find("-k-no")

    # Replace the substring with "s2000"
    modified_url = url[:start_index] + "s2000" + url[end_index:]
    return modified_url
