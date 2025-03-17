// Allow for order cards selected to be known so they add in order
let selectionOrder = [];

// Limit the amount of cards a player can select to 3 and track selection order
function limitSelections(checkbox) {
    const maxAllowed = 3;
    let checkboxes = document.getElementsByName('selected_cards');
    let checked = document.querySelectorAll('input[name="selected_cards"]:checked');
    
    if (checkbox.checked) {
        // If checkbox is checked, add to selection order
        selectionOrder.push(checkbox.value);
    } else {
        // If checkbox is unchecked, remove from selection order
        const index = selectionOrder.indexOf(checkbox.value);
        if (index > -1) {
            selectionOrder.splice(index, 1);
        }
    }
    
    // Enforce maximum limit
    if (checked.length > maxAllowed) {
        checkbox.checked = false;
        // Also remove from selection order if we exceeded limit
        const index = selectionOrder.indexOf(checkbox.value);
        if (index > -1) {
            selectionOrder.splice(index, 1);
        }
    }
    
    // Update hidden fields with the current order
    updateOrderFields();
}

// Update hidden fields with the current selection order
function updateOrderFields() {
    // Remove any existing order fields
    const existingFields = document.querySelectorAll('.order-field');
    existingFields.forEach(field => field.remove());
    
    // Create new fields for the current order
    const form = document.querySelector('form');
    
    for (let i = 0; i < selectionOrder.length; i++) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'card_order';
        hiddenField.value = selectionOrder[i];
        hiddenField.className = 'order-field';
        form.appendChild(hiddenField);
    }
}

// Check if the player has selected exactly 3 cards
function lessThanThree() {
    let checked = document.querySelectorAll('input[name="selected_cards"]:checked');
    console.log(checked.length);
    if (checked.length < 3) {
        alert("You must select 3 cards to update your deck.");
        return false;
    }
    
    // Ensure we have exactly 3 cards in the order
    if (selectionOrder.length > 3) {
        selectionOrder = selectionOrder.slice(0, 3);
    }
    
    // Final update of order fields before submission
    updateOrderFields();
    return true;
}

// Initialize selection order from already checked boxes when page loads
document.addEventListener('DOMContentLoaded', function() {
    let checkedBoxes = document.querySelectorAll('input[name="selected_cards"]:checked');
    checkedBoxes.forEach(box => {
        selectionOrder.push(box.value);
    });
    
    // Initialize hidden fields
    updateOrderFields();
});