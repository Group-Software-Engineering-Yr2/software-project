//todo comment the shit out of this
document.addEventListener("DOMContentLoaded", function () {
    const cooldownElement = document.getElementById("gym-cooldown-value");
    const gymRadius = 500;
    if (cooldownElement) {
        let cooldownEndTime = parseInt(cooldownElement.getAttribute("data-cooldown"), 10);
        function formatTime(remainingSeconds) {
            if (remainingSeconds <= 0) return "None, ready to battle!";
            const minutes = Math.floor(remainingSeconds / 60);
            const seconds = Math.floor(remainingSeconds % 60);
            return `${minutes}m ${seconds}s`;
        }
        
        function updateCooldown() {
            const now = Math.floor(Date.now() / 1000);
            const remainingTime = cooldownEndTime - now;
            
            if (remainingTime > 0) {
                cooldownElement.textContent = formatTime(remainingTime);
                setTimeout(updateCooldown, 1000);
            } else {
                cooldownElement.textContent = "0s, ready to battle!";
            }
        }
        updateCooldown();
    }

    // Check if geolocation is supported by the browser
    if ("geolocation" in navigator) {
        // Prompt user for permission to access their location
        navigator.geolocation.getCurrentPosition(
        // Success callback function
        (position) => {
        // Get the user's latitude and longitude coordinates
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;
        const result = isWithinRadius(gymLatitude, gymLongitude, gymRadius, userLat, userLng);
        if (result.isInRange) {
            if (cooldownElement.textContent === "0s, ready to battle!") {
                if(gymTeam != playerTeam) {
                    //User is in range of the radius of the gym and the gym is not on cooldown
                    document.getElementById("start-battle").addEventListener("click", function() {
                    window.location.href = '/gym-battle/' + gymID;
                    });
                } else {
                    //User is in range of the radius of the gym and the gym is not on cooldown but the gym belongs to the user's team
                    document.getElementById("start-battle").addEventListener("click", function() {
                    alert("You cannot battle this gym as it is owned by your team!");
                    });
                }
            } else {
                //User is in range of the radius of the gym but the gym is on cooldown
                document.getElementById("start-battle").addEventListener("click", function() {
                alert("You cannot battle this gym as there is a cooldown!");
                });
            } 
        } else {
            //User is not in range of the radius of the gym
            document.getElementById("start-battle").addEventListener("click", function() {
                alert(`You cannot battle this gym as you are not in range. \nYou are ${result.distance} meters away.`);
            });
        }
        },
        // Error callback function
        (error) => {
        // Handle errors, e.g. user denied location sharing permissions
         console.error("Error getting user location:", error);
        }
        );
    } else {
        // Geolocation is not supported by the browser
        console.error("Geolocation is not supported by this browser.");
    }

});


function isWithinRadius(gymLat, gymLon, gymRadius, userLat, userLon) {
    // Convert to radians
    const toRad = (x) => x * Math.PI / 180;
    
    // Earth's radius in meters
    const R = 6371000;
 
    const gymLatRad = toRad(gymLat);
    const gymLonRad = toRad(gymLon);
    const userLatRad = toRad(userLat);
    const userLonRad = toRad(userLon);
 
    // Calculate differences
    const dLat = userLatRad - gymLatRad;
    const dLon = userLonRad - gymLonRad;
 
    // Haversine formula
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(gymLatRad) * Math.cos(userLatRad) * 
              Math.sin(dLon/2) * Math.sin(dLon/2);
              
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c; // Distance in meters
 
    return {
        distance: Math.round(distance), // Rounded distance in meters
        isInRange: distance <= gymRadius
    };
} 
