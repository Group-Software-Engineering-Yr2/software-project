// Limit the amount of cards a player can select to 3
function limitSelections(checkbox) {
    const maxAllowed = 3;
    let checkboxes = document.getElementsByName('selected_cards');
    let checked = document.querySelectorAll('input[name="selected_cards"]:checked');

    if (checked.length > maxAllowed) {
        checkbox.checked = false;
    }
}

// Check if the player has selected 3 cards
function lessThanThree() {
    let checked = document.querySelectorAll('input[name="selected_cards"]:checked');
    console.log(checked.length);
    if (checked.length < 3) {
        alert("You must select 3 cards to update your deck.");
        return false;
    }
    return true;
}