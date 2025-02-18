
document.addEventListener("DOMContentLoaded", function () {
    let cardImage = document.querySelectorAll(".clollected-cards");

    playerCards.forEach(playerCards => {
        if (use_count > 0){
            let isUnlocked = card.getAttribute("data-unlocked") === "true";
            let cardImage = card.getAttribute("data-card-src");
        }
        else {
            let isUnlocked = card.getAttribute("data-unlocked") === "false";
            let blankImage;
            if (cardType === 0) {
                blankImage = "/static/images/profile/PlasticBlankBorder.png";
            } else if (cardType === 1) {
                blankImage = "/static/images/profile/RecycleBlankBorder.png";
            } else {
                blankImage = "/static/images/profile/PlantBlankBorder.png";
            }
        
        }

        card.src = isUnlocked ? cardImage : blankImage;

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
