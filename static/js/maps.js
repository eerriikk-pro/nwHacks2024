// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

// Dynamically load the Google Maps API using the API key
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 49.266, lng: -123.243 },
        zoom: 15,
        mapTypeId: "roadmap",
    });

    const infowindow = new google.maps.InfoWindow();
    const bounds = new google.maps.LatLngBounds();

    // Set up the starting marker
    const startingLocation = { lat: 49.266, lng: -123.243 }; // Replace with your desired coordinates
    const startingMarker = new google.maps.Marker({
        map: map,
        position: startingLocation
    });

    // You can set a default info window for the starting marker or fetch details like in the original code
    google.maps.event.addListener(startingMarker, "click", () => {
        infowindow.setContent('<div><strong>Starting Location</strong><br>Place details here.</div>');
        infowindow.open(map, startingMarker);
    });

    bounds.extend(startingLocation);

    // Create the search box and link it to the UI element.
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds());
    });

    let markers = [];

    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();

        if (places.length === 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach((marker) => marker.setMap(null));
        markers = [];

        // For each place, get the icon, name and location.
        const bounds = new google.maps.LatLngBounds();

        places.forEach((place) => {
            if (!place.geometry || !place.geometry.location) {
                console.log("Returned place contains no geometry");
                return;
            }

            // Create a marker for each place.
            const marker = new google.maps.Marker({
                map,
                position: place.geometry.location,
                title: place.name
            });

            markers.push(marker);

            google.maps.event.addListener(marker, "click", () => {
                const content = document.createElement("div");
                const nameElement = document.createElement("h2");
                nameElement.textContent = place.name;
                content.appendChild(nameElement);

                const placeIdElement = document.createElement("p");
                placeIdElement.textContent = place.place_id;
                content.appendChild(placeIdElement);

                const placeAddressElement = document.createElement("p");
                placeAddressElement.textContent = place.formatted_address;
                content.appendChild(placeAddressElement);

                // Add a search menus hyperlink
                const menuLink = document.createElement("a");
                menuLink.href = "#"; // Placeholder href, should be replaced with actual link
                menuLink.textContent = "Search menus";
                menuLink.onclick = function() {
                    handlePlaceId(place.place_id);
                    return false; // Prevent default link behavior
                };
                content.appendChild(menuLink);


                infowindow.setContent(content);
                infowindow.open(map, marker);
            });

            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
    map.fitBounds(bounds);
}

window.initMap = initMap;

// Dynamically load the Google Maps API using the API key
function loadGoogleMapsApi() {
    var script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&callback=initMap&libraries=places&v=weekly`;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
}

window.onload = loadGoogleMapsApi;
