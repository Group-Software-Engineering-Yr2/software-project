// map functionality
var map = L.map('map').setView([50.73514962, -3.53428346], 13);
var testmarker = L.marker([50.73514962, -3.53428346]).addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
