// Wait for the content to be fully loaded before executing any functions
document.addEventListener("DOMContentLoaded", function () {
    // Get cooldown element from HTML template
    const cooldownElement = document.getElementById("gym-cooldown-value");
    // Set gym radius value to ensure user is within certain bounds
    const gymRadius = 200;
    // If the cooldown element exists on the template
    if (cooldownElement) {
        // Get the total cooldown time from the data attribute passed by the backend python code
        let cooldownEndTime = parseInt(cooldownElement.getAttribute("data-cooldown"), 10);
        // Format the time in minutes and seconds
        function formatTime(remainingSeconds) {
            if (remainingSeconds <= 0) return "0s, ready to battle!";
            const minutes = Math.floor(remainingSeconds / 60);
            const seconds = Math.floor(remainingSeconds % 60);
            return `${minutes}m ${seconds}s`;
        }
        // Update the cooldown time every second to shoe the user live time remaining
        function updateCooldown() {
            // Get the current time in seconds
            const now = Math.floor(Date.now() / 1000);
            // Calculate the remaining time
            const remainingTime = cooldownEndTime - now;
            
            // If the remaining time is greater than 0, update the cooldown element
            if (remainingTime > 0) {
                cooldownElement.textContent = formatTime(remainingTime);
                setTimeout(updateCooldown, 1000);
            } else {
                cooldownElement.textContent = "0s, ready to battle!";
            }
        }
        // Call the updateCooldown function to start the countdown
        updateCooldown();
    }
    
    // Code from geolocation
    // Check if geolocation is supported by the browser
    if ("geolocation" in navigator) {
        // Prompt user for permission to access their location
        navigator.geolocation.getCurrentPosition(
        // Success callback function
        (position) => {
        // Get the user's latitude and longitude coordinates
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;
        // Returns object of distance and if user is within the radius of the gym
        const result = isWithinRadius(gymLatitude, gymLongitude, gymRadius, userLat, userLng);
        
        // If user is within range
        if (result.isInRange) {
            // Check if the gym is on cooldown
            if (cooldownElement.textContent === "0s, ready to battle!") {
                // Check if the user is on the same team as the gym
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
         alert("Error getting user location. Please enable location services to battle gyms.");
        }
        );
    } else {
        // Geolocation is not supported by the browser
        alert ("Geolocation is not supported by this browser, please try a different one.");
    }

});

// Function to handle the user's location and the gym's location
function isWithinRadius(gymLat, gymLon, gymRadius, userLat, userLon) {
    // Convert to radians
    const toRad = (x) => x * Math.PI / 180;
    
    // Earth's radius in meters
    const R = 6371000;
 
    // Convert gym coordinates to radians
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
        isInRange: distance <= gymRadius // Boolean if user is within the radius
    };
} 
