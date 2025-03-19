document.addEventListener('DOMContentLoaded', function() {
    // creating map object
    var map = L.map('map', {minZoom: 13}).locate({setView: true, maxZoom: 25});
    
    // creating map tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    
    // getting locate button and adding function to center on user 
    let locateButton = document.getElementById("locateButton");
    locateButton.addEventListener("click", function(){
        map.locate({setView: true});
    })

    // creating custom user location icon
    var userLocationIcon = L.icon({
        iconUrl: 'static/images/backend/homePage/userLocationMarker.png',
        iconSize: [40, 40],
    });
    
    // Store the current circle object globally
    var currentCircle = null;

    // function to add marker on user location
    function onLocationFound(e) {
        var radius = e.accuracy; 
        var playerMarker = L.marker(e.latlng, {icon: userLocationIcon}).addTo(map).bindPopup("This is you! (within " + Math.round(radius) + "m)");
        
        // making radius on player
        playerMarker.on('click', function (e) {
            // If there's already a circle, remove it
            if (currentCircle) {
                map.removeLayer(currentCircle);
            }

            // Create a new circle
            currentCircle = L.circle(e.latlng, {
                radius: Math.round(radius),
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.1,
            }).addTo(map);
        });
    }

    // moving map to user location on startup
    map.on('locationfound', onLocationFound);


    // creating custom marker objects
    var reduceMarker = L.icon({iconUrl: 'static/images/teams/reduce.png', iconSize: [30, 30]});
    var reuseMarker = L.icon({iconUrl: 'static/images/teams/Reuse.png', iconSize: [30, 30]});
    var recycleMarker = L.icon({iconUrl: 'static/images/teams/Recycle.png', iconSize: [30, 30]});
    var fossilMarker = L.icon({iconUrl: 'static/images/teams/Factory.png', iconSize: [30, 30]});

    // Getting all gym locations and adding markers (no AJAX)
    gyms.forEach(gym => {
        // getting the current gym owner
        var ownerTeam = gym.owning_player__profile__team_name__name;
        var marker;

        // checking which team, adding corresponding marker
        console.log(ownerTeam);
        if (ownerTeam == "Reduce") {
            marker = L.marker([gym.latitude, gym.longitude], {icon: reduceMarker}).addTo(map);
        } else if (ownerTeam == "Recycle") {
            marker = L.marker([gym.latitude, gym.longitude], {icon: recycleMarker}).addTo(map);
        } else if (ownerTeam == "Reuse") {
            marker = L.marker([gym.latitude, gym.longitude], {icon: reuseMarker}).addTo(map);
        } else {
            marker = L.marker([gym.latitude, gym.longitude], {icon: fossilMarker}).addTo(map);
        }

        marker.bindPopup(`<b>${gym.name}</b>`);

        // Adding click event to show radius circle
        marker.on('click', function () {
            // If there's already a circle, remove it
            if (currentCircle) {
                map.removeLayer(currentCircle);
            }

            // Create a new circle
            currentCircle = L.circle([gym.latitude, gym.longitude], {
                radius: 200,
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.1,
            }).addTo(map);
        });
    });

    // Function to remove gym radius when clicking anywhere else
    function removeGymRadius() {
        // If a circle exists, remove it
        if (currentCircle) {
            map.removeLayer(currentCircle);
            currentCircle = null;
        }
    }

    // Remove gym radius when clicking anywhere else on the map
    map.on('click', removeGymRadius);
})