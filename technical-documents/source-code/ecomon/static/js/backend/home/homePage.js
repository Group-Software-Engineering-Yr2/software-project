document.addEventListener('DOMContentLoaded', function() {
    // creating map object
    var map = L.map('map', {minZoom: 13}).locate({setView: true, maxZoom: 25});
    
    // creating map tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // aligning locate button correctly
    // getting edge button
    const rightmostButton = document.querySelector('.buttons-container .button:last-child');
    const locateButtonContainer = document.getElementById('locateButton-container');

    // finding offset
    let buttonRect = rightmostButton.getBoundingClientRect();
    let rightOffset = window.innerWidth - buttonRect.right;

    // setting offset
    locateButtonContainer.style.left = `${rightOffset}px`;
    
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
    
    // function to add marker on user location
    function onLocationFound(e) {
        var radius = e.accuracy; 
        L.marker(e.latlng, {icon: userLocationIcon}).addTo(map).bindPopup("This is you! (within " + Math.round(radius) + "m)");
    }

    // moving map to user location on startup
    map.on('locationfound', onLocationFound);

    // Getting all gym locations and adding markers (no AJAX)
    gyms.forEach(gym => {
        var marker = L.marker([gym.latitude, gym.longitude]).addTo(map);
        marker.bindPopup(`<b>${gym.name}</b>`);
    })   
});
