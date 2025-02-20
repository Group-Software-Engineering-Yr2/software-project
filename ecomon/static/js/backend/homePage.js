document.addEventListener('DOMContentLoaded', function() {
    // creating map object
    var map = L.map('map', {minZoom: 15}).locate({setView: true, maxZoom: 25});

    // creating map tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    
    // creating custom user location icon
    var userLocationIcon = L.icon({
        iconUrl: 'static/images/backend/homePage/userLocationMarker.png',
        iconSize: [40, 40],
    });
    
    // function to add marker on user location
    function onLocationFound(e) {
        var radius = e.accuracy; 
        L.marker(e.latlng, {icon: userLocationIcon}).addTo(map).bindPopup("This is you! (within " + Math.round(radius) + "m)").openPopup();
    }

    map.on('locationfound', onLocationFound);

    // getting all gym locations and adding markers
    fetch('/get_gym_locations/')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data.forEach(gym => {
                var marker = L.marker([gym.latitude, gym.longitude]).addTo(map);
                marker.bindPopup(`<b>${gym.name}</b>`).openPopup();
            });
        })
        .catch(error => console.error('Error fetching gym locations:', error));
        
});