
document.addEventListener("DOMContentLoaded", function () {
    let cardImage = document.querySelectorAll(".collected-cards");

    playerCards.forEach(playerCards => {
        let cardImage = playerCards.getAttribute("data-card-src");
        let cardType = playerCards.getAttribute("data-card-type");
        let useCount = parseInt(card.getAttribute("data-use-count"));
        let blankImage;

        // Determine which blank border to show based on card type
        if (cardType === "0") {
            blankImage = "/static/images/profile/PlasticBlankBorder.png";
        } else if (cardType === "1") {
            blankImage = "/static/images/profile/RecycleBlankBorder.png";
        } else {
            blankImage = "/static/images/profile/PlantBlankBorder.png";
        }

        // Show actual card image if use_count > 0, otherwise show blank border
        card.src = useCount > 0 ? cardImage : blankImage;

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
