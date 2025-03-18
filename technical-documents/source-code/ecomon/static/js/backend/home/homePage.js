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
    
    // function to add marker on user location
    function onLocationFound(e) {
        var radius = e.accuracy; 
        L.marker(e.latlng, {icon: userLocationIcon}).addTo(map).bindPopup("This is you! (within " + Math.round(radius) + "m)");
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
        // checking which team, adding corresponding marker
        console.log(ownerTeam);
        if (ownerTeam == "Reduce") {
            var marker = L.marker([gym.latitude, gym.longitude], {icon: reduceMarker}).addTo(map);
            marker.bindPopup(`<b>${gym.name}</b>`);
        } else if (ownerTeam == "Recycle") {
            var marker = L.marker([gym.latitude, gym.longitude], {icon: recycleMarker}).addTo(map);
            marker.bindPopup(`<b>${gym.name}</b>`);
        } else if (ownerTeam == "Reuse") {
            var marker = L.marker([gym.latitude, gym.longitude], {icon: reuseMarker}).addTo(map);
            marker.bindPopup(`<b>${gym.name}</b>`);            
        } else {
            var marker = L.marker([gym.latitude, gym.longitude], {icon: fossilMarker}).addTo(map);
            marker.bindPopup(`<b>${gym.name}</b>`);     
        }
    })
});
