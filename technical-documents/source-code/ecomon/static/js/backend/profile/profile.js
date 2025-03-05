document.addEventListener('DOMContentLoaded', function() {
    // Get all card container elements
    const cardCells = document.querySelectorAll('.cardTable td');
    
    // Process each cell to add the flip functionality
    cardCells.forEach(cell => {
        const originalImg = cell.querySelector('img');
        if (!originalImg) return;
        
        // Skip processing if the card is not obtained (has "Blank" in the alt text)
        if (originalImg.alt.includes('Blank')) return;
        
        // Create the card container structure
        const cardContainer = document.createElement('div');
        cardContainer.className = 'card-container';
        
        const cardInner = document.createElement('div');
        cardInner.className = 'card-inner';
        
        // Create front of card
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';
        
        // Create back of card
        const cardBack = document.createElement('div');
        cardBack.className = 'card-back';
        
        // Get the card type from the data attribute (if available)
        let cardType = originalImg.dataset.cardType;
        
        // If data attribute isn't available, try to determine from other clues
        if (!cardType) {
            const imgSrc = originalImg.src.toLowerCase();
            
            if (imgSrc.includes('recycle')) {
                cardType = '2';
            } else if (imgSrc.includes('plant')) {
                cardType = '3';
            } else {
                cardType = '1'; // Default to plastic
            }
        }
        
        // Move the original image into the front
        originalImg.remove();
        cardFront.appendChild(originalImg);
        
        // Create the back image based on card type
        const backImg = document.createElement('img');
        
        // Set the appropriate back image based on card type
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
        
        cardBack.appendChild(backImg);
        
        // Add front and back to the inner container
        cardInner.appendChild(cardFront);
        cardInner.appendChild(cardBack);
        
        // Add inner container to the main container
        cardContainer.appendChild(cardInner);
        
        // Replace the cell's content with our new card container
        cell.innerHTML = '';
        cell.appendChild(cardContainer);
        
        // Add click event to flip the card
        cardContainer.addEventListener('click', function() {
            this.classList.toggle('flipped');
        });
    });
});