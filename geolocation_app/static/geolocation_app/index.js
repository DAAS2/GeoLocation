document.addEventListener('DOMContentLoaded', function() {
    trackLocation()
    Chat();
});

// initialise map
async function initMap(position) {
    // fetch the childs location that has been saved 
    try {
        const response = await fetch('/save_child_location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            // add lat and lng to body
            body: JSON.stringify({ lat: position.coords.latitude, lng: position.coords.longitude })
        });


        console.log(position.coords.latitude, position.coords.longitude);
        
        // User location cords
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        // create google map with user location
        const map = new google.maps.Map(document.getElementById("map"), {
            mapId: "8e0a97af9386fef",
            zoom: 15,
            center: userLocation,
            disableDefaultUI: true
        });

        console.log(userLocation);
        
        // create marker 
        const marker = new google.maps.Marker({
            position: userLocation,
            map: map,
        });
    } 
    
    catch (error) {
        console.log('An error occurred while loading the map: ' + error.message);
    }
}

// track childs location
function trackLocation() {
    // return childs live location
    return navigator.geolocation.watchPosition(
        (position) => initMap(position),
        (error) => {
            console.error("Geolocation error:", error);
            alert("Geolocation failed. Please enable location services and try again.");
        }, 
        {
            enableHighAccuracy: true,
            maximumAge: 0
        }
    );
    // happen every second
    setInterval(trackLocation, 1000);
}


// Chat 
function Chat() {
    // connext to chat
    try {
        const chatSocket = new WebSocket("ws://" + window.location.host + "/");

        // if connected succesfully
        chatSocket.onopen = function(e) {
            console.log("The connection was setup successfully!");
        };

        chatSocket.onclose = function(e) {
            console.log("WebSocket connection was closed unexpectedly.");
        };

        chatSocket.onerror = function(error) {
            console.log("An error occurred with the WebSocket connection.");
        };

        // get message text
        document.querySelector("#id_message_send_input").focus();
        document.querySelector("#id_message_send_input").onkeyup = function(e) {
            if (e.keyCode == 13) {
                document.querySelector("#id_message_send_button").click();
            }
        };
        
        // when button clicked then send message and username
        document.querySelector("#id_message_send_button").onclick = function(e) {
            var messageInput = document.querySelector("#id_message_send_input").value;

            if (messageInput.trim() === "") {
                alert("Message cannot be empty.");
                return;
            }

            chatSocket.send(JSON.stringify({ message: messageInput, username: "{{request.user.username}}" }));
        };

        // parse the message and username and create the write css for it
        chatSocket.onmessage = function(e) {
            try {
                const data = JSON.parse(e.data);
                var div = document.createElement("div");
                div.innerHTML = '<div class="card message-card mb-2 user-message">' + 
                                '<div class="card-body d-flex justify-content-between">' + 
                                    '<p class="card-text mb-0" >' + data.message + '</p>' + 
                                    '<p class="card-text text-muted mb-0 timestamp small">' + new Date().toISOString().slice(0, 19).replace('T', ' ') + '</p>' +
                                '</div>' + 
                                '</div>';
                document.querySelector("#id_message_send_input").value = "";
                document.querySelector("#id_chat_item_container").appendChild(div);
            } catch (error) {
                console.log('An error occurred while processing a received message.');
            }
        };
    } catch (error) {
        console.log('An error occurred while setting up the chat system.');
    }
}
