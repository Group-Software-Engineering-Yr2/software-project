// map functionality
document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([50.73514962, -3.53428346], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

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