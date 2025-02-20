// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    setPlayerActiveCard(activePlayerCard);
    setPlayerCardSlot1(playerCardSlot1);
    setPlayerCardSlot2(playerCardSlot2);
    setOpponentActiveCard(activeOpponentCard);
    setOpponentCardSlot1(opponentCardSlot1);
    setOpponentCardSlot2(opponentCardSlot2);
    isPlayerTurn = true;

    // Add event listeners
    document.getElementById('player-move-1').addEventListener('click', function() {
        // if (battleState.isPlayerTurn && !checkGameOver(battleState)) {
        
        handlePlayerTurn(1);

        // }
    });

    document.getElementById('player-move-2').addEventListener('click', function() {
        // if (battleState.isPlayerTurn && !checkGameOver(battleState)) {
            handlePlayerTurn(2);
        // }
    });

    document.getElementById('player-retreat-1').addEventListener('click', function() {
        // if (battleState.isPlayerTurn && !checkGameOver(battleState)) {
            // document.getElementById('player-active-card-icon').src = playerCard2Icon;
            setPlayerActiveCard(playerCardSlot1);
            setPlayerCardSlot1(activePlayerCard);
            let temp = activePlayerCard;
            activePlayerCard = playerCardSlot1;
            playerCardSlot1 = temp;
        // }
    });

    document.getElementById('player-retreat-2').addEventListener('click', function() {
        // if (battleState.isPlayerTurn && !checkGameOver(battleState)) {
            // document.getElementById('player-active-card-icon').src = playerCard2Icon;
            setPlayerActiveCard(playerCardSlot2);
            setPlayerCardSlot2(activePlayerCard);
            let temp = activePlayerCard;
            activePlayerCard = playerCardSlot2;
            playerCardSlot2 = temp;
        // }
    });
});


function setPlayerActiveCard(card){
    document.getElementById('player-active-card-icon').src = card.image;
    document.getElementById('player-hp').textContent = `HP: ${card.health_points}`;
    document.getElementById('player-active-card-name').textContent = card.name;
    document.getElementById('ability-power-1').textContent = card.ability_power_1 + " Damage";
    let ability2 = document.getElementById('ability-power-2').textContent = card.ability_power_2;
    if (ability2 > 0) {
        document.getElementById('ability-power-2').textContent = card.ability_power_2 + " Damage";
    } else {
        document.getElementById('ability-power-2').textContent = "+ " + card.ability_self_power_2 + " Health";
    }
}

function setPlayerCardSlot1(card){
    document.getElementById('player-slot-1-icon').src = card.image;
}

function setPlayerCardSlot2(card){
    document.getElementById('player-slot-2-icon').src = card.image;
}

function setOpponentActiveCard(card){
    document.getElementById('opponent-active-card-icon').src = card.image;
    document.getElementById('opponent-hp').textContent = `HP: ${card.health_points}`;
    document.getElementById('opponent-active-card-name').textContent = card.name;
}

function setOpponentCardSlot1(card){
    document.getElementById('opponent-slot-1-icon').src = card.image;
}

function setOpponentCardSlot2(card){
    document.getElementById('opponent-slot-2-icon').src = card.image;
}

// Handle player's turn
function handlePlayerTurn(moveChoice) {
    isPlayerTurn = false;
    //Handles First Move Button Click (First sustainAbility)
    if (moveChoice === 1) {
        let result = activeOpponentCard.health_points - activePlayerCard.ability_power_1;
        if (result < 0) result = 0;
        activeOpponentCard.health_points = result;
        document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

        // Add to battle log
        let battleLog = document.querySelector('.battle-log');
        battleLog.innerHTML += `<p>Player used Ability ` + moveChoice + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        // Add logic for new card to be put in

    //Handles Second Move Button Click (Second sustainAbility)
    } else if (moveChoice === 2) {
        // If the second sustainAbility is a damage move
        if (activePlayerCard.ability_power_2 > 0) {
            let result = activeOpponentCard.health_points - activePlayerCard.ability_power_2;
            if (result < 0) result = 0;
            activeOpponentCard.health_points = result;
            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
            
            // Add to battle log
            let battleLog = document.querySelector('.battle-log');
            battleLog.innerHTML += `<p>Player used Ability ` + moveChoice + ` for ${activePlayerCard.ability_power_2} damage!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;

        // If the second sustainAbility is a heal move
        } else {
            let result = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
            activePlayerCard.health_points = result;
            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

            // Add to battle log
            let battleLog = document.querySelector('.battle-log');
            battleLog.innerHTML += `<p>Player used Ability ` + moveChoice + ` to heal ${activePlayerCard.ability_self_power_2} health!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;

        }
    } else {
        alert("Invalid move choice");
    }

    // if (!checkGameOver(battleState)) {
    //     // Start opponent's turn after a delay
    //     setTimeout(() => {
    //         handleOpponentTurn(battleState);
    //     }, 1000);
    // }

    // Update display
    setOpponentActiveCard(activeOpponentCard);
    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

    // Add to battle log
    // const battleLog = document.querySelector('.battle-log');
    // battleLog.innerHTML += `<p>Player used Ability ` + moveChoice + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
    // battleLog.scrollTop = battleLog.scrollHeight;
}

// Handle opponent's turn
function handleOpponentTurn(battleState) {
    const moveChoice = Math.random() < 0.5 ? 1 : 2;
    
    if (moveChoice === 1) {
        // Use ability 1 (damage)
        battleState.player.currentHP -= battleState.opponent.abilities.ability1;
        
        // Update display
        document.getElementById('player-hp').textContent = `HP: ${battleState.player.currentHP}`;
        
        // Add to battle log
        const battleLog = document.querySelector('.battle-log');
        battleLog.innerHTML += `<p>Opponent used Ability 1 for ${battleState.opponent.abilities.ability1} damage!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
    } else {
        if (battleState.opponent.abilities.ability2Type === 'heal') {
            const newHP = battleState.opponent.currentHP + battleState.opponent.abilities.ability2;
            const healingAmount = newHP - battleState.opponent.currentHP;
            battleState.opponent.currentHP = newHP;
            
            // Update display
            document.getElementById('opponent-hp').textContent = `HP: ${battleState.opponent.currentHP}`;
            
            // Add to battle log
            const battleLog = document.querySelector('.battle-log');
            battleLog.innerHTML += `<p>Opponent healed for ${healingAmount} HP!</p>`;
        } else {
            battleState.player.currentHP -= battleState.opponent.abilities.ability2;
            
            // Update display
            document.getElementById('player-hp').textContent = `HP: ${battleState.player.currentHP}`;
            
            // Add to battle log
            const battleLog = document.querySelector('.battle-log');
            battleLog.innerHTML += `<p>Opponent used Ability 2 for ${battleState.opponent.abilities.ability2} damage!</p>`;
        }
        
        // Scroll battle log
        const battleLog = document.querySelector('.battle-log');
        battleLog.scrollTop = battleLog.scrollHeight;
    }

    // Check for game over and set back to player's turn
    if (!checkGameOver(battleState)) {
        battleState.isPlayerTurn = true;
    }
}

// function checkGameOver(battleState) {
//     if (battleState.player.currentHP <= 0) {
//         const battleLog = document.querySelector('.battle-log');
//         battleLog.innerHTML += `<p>Player's active card has fainted!</p>`;
//         battleLog.scrollTop = battleLog.scrollHeight;
//         alert("Your card has fainted! Game Over!");
//         disableButtons();
//         return true;
//     }
//     if (battleState.opponent.currentHP <= 0) {
//         const battleLog = document.querySelector('.battle-log');
//         battleLog.innerHTML += `<p>Opponent's active card has fainted!</p>`;
//         battleLog.scrollTop = battleLog.scrollHeight;
//         alert("Opponent's card has fainted! You win!");
//         disableButtons();
//         return true;
//     }
//     return false;
// }

function disableButtons() {
    document.getElementById('player-move-1').disabled = true;
    document.getElementById('player-move-2').disabled = true;
    document.getElementById('player-retreat-1').disabled = true;
    document.getElementById('player-retreat-2').disabled = true;
}

//Function that adds moves and events in the battle log div
function addLog(string){
    // Locate id battle-log
    battleLog = document.getElementById('battle-log').textContent = string;
    // Create new p element
    let p = document.createElement('p');
    p.textContent = string;
    // Append p to div battle log
    battleLog.appendChild(p);
}