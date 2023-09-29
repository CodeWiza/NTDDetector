document.addEventListener("DOMContentLoaded", function () {
    // Check if the Geolocation API is available
    if ("geolocation" in navigator) {
        // Request location permission immediately when the page loads
        document.getElementById("getLocation").addEventListener("click", getLocation);
    } else {
        // Geolocation is not supported by this browser
        document.getElementById("location_text").innerHTML = "Geolocation is not supported by this browser.";
    }
});

function getLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var new_latitude = position.coords.latitude;
            var new_longitude = position.coords.longitude;
           
            var hiddenLatitudeInput = document.getElementById("latitude");
            var hiddenLongitudeInput = document.getElementById("longitude");
            hiddenLatitudeInput.value = new_latitude;
            hiddenLongitudeInput.value = new_longitude;


/*  If want to send value from js to django( not used )
            $.ajax({
                type: "POST",
                url: "prediction_form/save", // Replace with the correct URL
                data: formData,
                processData: false, // Prevent jQuery from processing the data
                contentType: false, // Prevent jQuery from setting a content type
                success: function (response) {
                    // Handle the response from the Django view here if needed.
                    console.log("Location data sent successfully:", response);
                },
                error: function (error) {
                    console.error("Error sending location data:", error);
                }
            });*/

            // You can send this latitude and longitude to your Django backend using an AJAX request.
            // Example: Send them to a Django view via a POST request for further processing.
        }, showError);
    }
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("location_text").innerHTML = "User denied the request for geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("location_text").innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("location_text").innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("location_text").innerHTML = "An unknown error occurred.";
            break;
    }
}

document.getElementById("uploadButton").addEventListener("click", function () {
    // Redirect to the dashboard page (replace with the actual URL)
    window.location.href = "/dashboard";
});
