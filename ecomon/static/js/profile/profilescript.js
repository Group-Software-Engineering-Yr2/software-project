document.addEventListener("DOMContentLoaded", function () {
    const cardTable = document.querySelector(".cardTable table");
    
    // Get data from script tags
    const allCards = JSON.parse(document.getElementById('cards-data').textContent);
    const playerCards = JSON.parse(document.getElementById('player-cards-data').textContent);
    
    // Create grid using allCards data
    let currentRow;
    allCards.forEach((card, index) => {
        if (index % 3 === 0) {
            currentRow = cardTable.insertRow();
        }
        
        let cell = currentRow.insertCell();
        let img = document.createElement('img');
        img.className = 'collected-cards';
        
        // Check if player has this card
        const playerCard = playerCards.find(pc => pc.cardId === card.id);
        const useCount = playerCard ? playerCard.useCount : 0;
        
        // Set image based on whether card is unlocked
        if (useCount > 0) {
            img.src = card.image;
        } else {
            // Set default border based on card type
            switch (parseInt(card.type)) {
                case 0:
                    img.src = "/static/images/profile/PlasticBlankBorder.png";
                    break;
                case 1:
                    img.src = "/static/images/profile/RecycleBlankBorder.png";
                    break;
                case 2:
                    img.src = "/static/images/profile/PlantBlankBorder.png";
                    break;
            }
        }
        
        cell.appendChild(img);

        // Example: Unlocking on Click (For Testing)
        card.addEventListener("click", function () {
            if (!isUnlocked) {
                isUnlocked = true;
                card.src = cardImage;
                card.setAttribute("data-unlocked", "true"); // Update attribute
            }
        });
    });
});
