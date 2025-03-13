document.addEventListener('DOMContentLoaded', function() {
    
    // Select all cells in cardTable (All obtained cards)
    const cardCells = document.querySelectorAll('.cardTable td');

    // Loop through each card
    cardCells.forEach(cell => {
        
        // gets image inside the card cell
        const originalImg = cell.querySelector('img');
        
        // Create a div element to act as the card container
        const cardContainer = document.createElement('div');
        cardContainer.className = 'card-container';

        // Create a div to hold both the front and back of the card
        const cardInner = document.createElement('div');
        cardInner.className = 'card-inner';

        // Create the front of the card
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';

        // Create the back of  card
        const cardBack = document.createElement('div');
        cardBack.className = 'card-back';

        // Try to get the card type from the data attribute of the image
        let cardType = originalImg.dataset.cardType;

        // If no data, make card type based on image source
        if (!cardType) {
            const imgSrc = originalImg.src.toLowerCase(); // Convert to lowercase for consistency
            
            // If the image filename contains "recycle" assign cardtype 2 which is recycle
            if (imgSrc.includes('recycle')) {
                cardType = '2';
            } 
            // If the image filename contains "plant", assign cardtype 3 which is plant
            else if (imgSrc.includes('plant')) {
                cardType = '3';
            } 
            // otherwise do plastic
            else {
                cardType = '1';
            }
        }

        // Remove the original image from the cell
        originalImg.remove();
        
        // Append the original image to the front of the card
        cardFront.appendChild(originalImg);

        // Create a new image element for the back of the card
        const backImg = document.createElement('img');

        // Set the back image source and alt text based on the determined card type
        if (cardType === '2') {
            backImg.src = "/static/images/backend/profile/backrecyclecard.png";
            backImg.alt = "Recycle Card Back";
        } else if (cardType === '3') {
            backImg.src = "/static/images/backend/profile/backplantcard.png";
            backImg.alt = "Plant Card Back";
        } else {
            backImg.src = "/static/images/backend/profile/backplasticcard.png";
            backImg.alt = "Plastic Card Back";
        }

        // Append the back image to the back side of the card
        cardBack.appendChild(backImg);

        // Append the front and back sides  to the inner container
        cardInner.appendChild(cardFront);
        cardInner.appendChild(cardBack);

        //Append the inner container to the main card container
        cardContainer.appendChild(cardInner);

        // Clear the existing content of the cell and replace it with new card container
        cell.innerHTML = '';
        cell.appendChild(cardContainer);

        // Add a click event for the 'flipping of a card'
        cardContainer.addEventListener('click', function() {
            // If the card is already flipped, remove the 'flipped' class
            if (this.classList.contains('flipped')) {
                this.classList.remove('flipped');
            } 
            // If the card is not flipped, add the 'flipped' class
            else {
                this.classList.add('flipped');
            }
            // Changed from toggle in hope older version of JS still work and run it
        });
    });
});
