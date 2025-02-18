document.addEventListener("DOMContentLoaded", function () {
    const cardTable = document.querySelector(".cardTable table");

    // Fetch both cards and player cards data
    Promise.all([
        fetch('/api/cards/'),
        fetch('/api/player-cards/')
    ])
    .then(responses => Promise.all(responses.map(r => r.json())))
    .then(([cardsData, playerCardsData]) => {
        const cards = cardsData.cards;
        const playerCards = playerCardsData.player_cards;

        // Create grid for each card
        let currentRow;
        cards.forEach((card, index) => {
            if (index % 3 === 0) {
                currentRow = cardTable.insertRow();
            }

            let cell = currentRow.insertCell();
            let img = document.createElement('img');
            img.className = 'collected-cards';

            // Find if player has this card
            const playerCard = playerCards.find(pc => pc.name === card.name);
            const useCount = playerCard ? playerCard.use_count : 0;

            if (useCount > 0) {
                img.src = `static/${card.image}`;
            } else {
                switch (parseInt(card.card_type)) {
                    case 1:
                        img.src = "static/images/profile/PlasticBlankBorder.png";
                        break;
                    case 2:
                        img.src = "static/images/profile/RecycleBlankBorder.png";
                        break;
                    case 0:
                        img.src = "static/images/profile/PlantBlankBorder.png";
                        break;
                }
            }

            cell.appendChild(img);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});