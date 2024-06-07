
document.addEventListener('DOMContentLoaded', function(){
    locateUser()

    async function initMap(position) {
        try {
            const response = await fetch('/save_child_location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                
                body: JSON.stringify({ lat: position.coords.latitude, lng: position.coords.longitude })
            });

               
        } catch (error) {
            console.error('Error:', error);
        }

        console.log(position.coords.latitude, position.coords.longitude)

        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        const map = new google.maps.Map(document.getElementById("map"), {
            mapId: "8e0a97af9386fef",
            zoom: 15,
            center: userLocation,
            disableDefaultUI: true
        });

        console.log(userLocation)
        const marker = new google.maps.Marker({
            position: userLocation,
            map: map,
        });
    }

    function locateUser() {
        console.log("Locating User Location")
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => initMap(position),
                (error) => {
                    console.error("Geolocation error:", error);
                    alert("Geolocation failed. Please enable location services and try again.");
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );

        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }


});