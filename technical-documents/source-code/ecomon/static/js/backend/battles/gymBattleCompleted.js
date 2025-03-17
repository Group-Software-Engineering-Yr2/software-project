// Load the DOM before running the script and check if any of the cards have expired
document.addEventListener('DOMContentLoaded', () => {
    // Listeners for the gym battle completed page
        document.getElementById('continueButton').addEventListener('click', () => {
            document.getElementById('decomposed-cards-overlay').style.display = 'none';
        });
});
