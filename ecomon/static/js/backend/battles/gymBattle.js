// Wait for the DOM to be fully loaded
//TODO: Add comments to explain wtf my JS is doing.
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
        if (isPlayerTurn) {
            handlePlayerTurn(1);
        }
    });

    document.getElementById('player-move-2').addEventListener('click', function() {
        if (isPlayerTurn) {
            handlePlayerTurn(2);
        }   
    });

    document.getElementById('player-retreat-1').addEventListener('click', function() {
        if (isPlayerTurn) {
            if (playerCardSlot1.health_points > 0) {
                handlePlayerTurn(3);
                setPlayerActiveCard(playerCardSlot1);
                setPlayerCardSlot1(activePlayerCard);
                let temp = activePlayerCard;
                activePlayerCard = playerCardSlot1;
                playerCardSlot1 = temp;
            } else {
                alert("Unable to retreat, the card in Slot 1 is dead!");
            }
        }
    });

    document.getElementById('player-retreat-2').addEventListener('click', function() {     
        if (isPlayerTurn) {
            if (playerCardSlot2.health_points > 0) {
                handlePlayerTurn(4);
                setPlayerActiveCard(playerCardSlot2);
                setPlayerCardSlot2(activePlayerCard);
                let temp = activePlayerCard;
                activePlayerCard = playerCardSlot2;
                playerCardSlot2 = temp;
            } else {
                alert("Unable to retreat, the card in Slot 2 is dead!");
            }   
        } 
    });
});


function setPlayerActiveCard(card){
    document.getElementById('player-active-card-icon').src = card.image;
    document.getElementById('player-hp').textContent = `HP: ${card.health_points}`;
    document.getElementById('player-active-card-name').textContent = card.name;
    document.getElementById('player-move-1').textContent = card.ability_name_1 + ": " + card.ability_power_1 + " Damage";
    if (card.ability_power_2 > 0 && card.ability_self_power_2 == 0) {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": " + card.ability_power_2 + " Damage";
    } else if (card.ability_power_2 > 0 && card.ability_self_power_2 > 0) {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": " + card.ability_power_2 + " Damage and +" + card.ability_self_power_2 + " Health";
    } else {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": +" + card.ability_self_power_2 + " Health";
    }
    document.getElementById('player-retreat-1').textContent = "Retreat "+ card.name + " for Bench Card 1";
    document.getElementById('player-retreat-2').textContent = "Retreat "+ card.name + " for Bench Card 2";
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
    let battleLog = document.querySelector('.battle-log');
    let swapped = false;
    //Handles First Move Button Click (First sustainAbility)
    if (moveChoice === 1) {
        let result = activeOpponentCard.health_points - activePlayerCard.ability_power_1;
        if (result <= 0) {
            result = 0;
            activeOpponentCard.health_points = result;
            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_1 + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;
            battleLog.innerHTML += `<p>` + opponent + `'s `+ activeOpponentCard.name + ` fainted!</p>`;
            swapped = checkOpponentDeadCard();
        } else {
            activeOpponentCard.health_points = result;
            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_1 + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;
        }
    //Handles Second Move Button Click (Second sustainAbility)
    } else if (moveChoice === 2) {
        // If the second sustainAbility is a damage move
        if (activePlayerCard.ability_power_2 > 0 && activePlayerCard.ability_self_power_2 == 0) {
            let result = activeOpponentCard.health_points - activePlayerCard.ability_power_2;
            if (result <= 0) {
                result = 0;
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
            
                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                battleLog.innerHTML += `<p>` + opponent + `'s `+ activeOpponentCard.name + ` fainted!</p>`;
                swapped = checkOpponentDeadCard();
            } else {
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
            }
        // If the second sustainAbility is a heal and damage move
        } else if (activePlayerCard.ability_power_2 > 0 && activePlayerCard.ability_self_power_2 > 0) {
            let result = activeOpponentCard.health_points - activePlayerCard.ability_power_2;
            let selfResult = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
            if (result <= 0) {
                result = 0;
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                activePlayerCard.health_points = selfResult;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage and healed ${activePlayerCard.ability_self_power_2} health!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                battleLog.innerHTML += `<p>` + opponent + `'s `+ activeOpponentCard.name + ` fainted!</p>`;
                swapped = checkOpponentDeadCard();
            } else {
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                activePlayerCard.health_points = selfResult;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage and healed + ${activePlayerCard.ability_self_power_2} health!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
            }
        // If the second sustainAbility is a heal move only
        } else {
            let result = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
            activePlayerCard.health_points = result;
            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + username + ` used `+ activePlayerCard.ability_name_2 + ` to heal ${activePlayerCard.ability_self_power_2} health!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;

        }
    } else if (moveChoice === 3) {
        // Handles retreat action for slot 1
        battleLog.innerHTML += `<p>` + username + ` retreated `+ activePlayerCard.name +` for `+ playerCardSlot1.name +`!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
    } else if (moveChoice === 4) {
        // Handles retreat action for slot 2
        battleLog.innerHTML += `<p>` + username + ` retreated `+ activePlayerCard.name +` for `+ playerCardSlot2.name +`!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
    }

    // Start opponent's turn after a delay
    // if (!swapped && !checkOpponentGameOver()) {
    //     setTimeout(() => {
    //         handleOpponentTurn();
    //     }, 1000);
    // } else {
    //     isPlayerTurn = true;
    // }
    if (!checkOpponentGameOver()) {
        setTimeout(() => {
            handleOpponentTurn();
        }, 1000);
    } else {
        isPlayerTurn = true;
    }
}

// Handle opponent's turn
function handleOpponentTurn() {
    let swapped = false;
    let battleLog = document.querySelector('.battle-log');
    const moveChoice = Math.random() < 0.5 ? 1 : 2;

    if (moveChoice === 1) {
        let result = activePlayerCard.health_points - activeOpponentCard.ability_power_1;
        if (result <= 0) {
            result = 0;
            activePlayerCard.health_points = result;
            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_1 + ` for ${activeOpponentCard.ability_power_1} damage!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;
            battleLog.innerHTML += `<p>` + username + `'s `+ activePlayerCard.name + ` fainted!</p>`;
            swapped = checkPlayerDeadCard();
        } else {
            activePlayerCard.health_points = result;
            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_1 + ` for ${activeOpponentCard.ability_power_1} damage!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;
        }
    } else if (moveChoice === 2) {
        // If the second sustainAbility is a damage move
        if (activeOpponentCard.ability_power_2 > 0 && activeOpponentCard.ability_self_power_2 == 0) {
            let result = activePlayerCard.health_points - activeOpponentCard.ability_power_2;
            if (result <= 0) {
                result = 0;
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
            
                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                battleLog.innerHTML += `<p>` + username + `'s `+ activePlayerCard.name + ` fainted!</p>`;
                swapped = checkPlayerDeadCard();
            } else {
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
            
                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
            }
        // If the second sustainAbility is a heal and damage move
        } else if (activeOpponentCard.ability_power_2 > 0 && activeOpponentCard.ability_self_power_2 > 0) {
            let result = activePlayerCard.health_points - activeOpponentCard.ability_power_2;
            let selfResult = activeOpponentCard.health_points + activeOpponentCard.ability_self_power_2;
            if (result <= 0) {
                result = 0;
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                activeOpponentCard.health_points = selfResult;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage and healed ${activeOpponentCard.ability_self_power_2} health!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                battleLog.innerHTML += `<p>` + username + `'s `+ activePlayerCard.name + ` fainted!</p>`;
                swapped = checkPlayerDeadCard();
            } else {
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                activeOpponentCard.health_points = selfResult;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage and healed ${activeOpponentCard.ability_self_power_2} health!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
            }
        // If the second sustainAbility is a heal move only
        } else {
            let result = activeOpponentCard.health_points + activeOpponentCard.ability_self_power_2;
            activeOpponentCard.health_points = result;
            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

            // Add to battle log
            battleLog.innerHTML += `<p>` + opponent + ` used `+ activeOpponentCard.ability_name_2 + ` to heal ${activeOpponentCard.ability_self_power_2} health!</p>`;
            battleLog.scrollTop = battleLog.scrollHeight;

        }
    }

    // Check for game over and set back to player's turn
    // if (!swapped) {   
    //     isPlayerTurn = true;
    // }  else {
    //     isPlayerTurn = false;
    //     setTimeout(() => {
    //         handleOpponentTurn();
    //     }, 1000);
    // }
    if (!checkPlayerGameOver()) {   
        isPlayerTurn = true;
    }  else {
        isPlayerTurn = false;
        setTimeout(() => {
            handleOpponentTurn();
        }, 1000);
    }
}

function checkOpponentDeadCard() {
    let battleLog = document.querySelector('.battle-log');
    if (opponentCardSlot1.health_points > 0) {
        setOpponentActiveCard(opponentCardSlot1);
        setOpponentCardSlot1(activeOpponentCard);
        let temp = activeOpponentCard
        activeOpponentCard = opponentCardSlot1;
        opponentCardSlot1 = temp;
        swapped = true;
        document.getElementById('opponent-slot-1-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + opponent + ` swapped `+ opponentCardSlot1.name + ` for ${activeOpponentCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        return true;

    } else if (opponentCardSlot2.health_points > 0) {
        setOpponentActiveCard(opponentCardSlot2);
        setOpponentCardSlot2(activeOpponentCard);
        let temp = activeOpponentCard;
        activeOpponentCard = opponentCardSlot2;
        opponentCardSlot2 = temp;
        swapped = true;
        document.getElementById('opponent-slot-2-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + opponent + ` swapped `+ opponentCardSlot2.name + ` for ${activeOpponentCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        return true;

    } else {
        document.getElementById('opponent-active-card-icon').classList.add('card-dead');
        alert("Opponent has no more cards! You win!");
        battleLog.innerHTML += `<p>` + opponent + ` has no more cards! You win!</p>`;
        completeGymBattle(true, gymID);
        disableButtons();
    }
    return false;
}

function checkPlayerDeadCard() {
    let battleLog = document.querySelector('.battle-log');
    if (playerCardSlot1.health_points > 0) {
        setPlayerActiveCard(playerCardSlot1);
        setPlayerCardSlot1(activePlayerCard);
        let temp = activePlayerCard
        activePlayerCard = playerCardSlot1;
        playerCardSlot1 = temp;
        swapped = true;
        document.getElementById('player-slot-1-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + username + ` swapped `+ playerCardSlot1.name + ` for ${activePlayerCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        return true;

    } else if (playerCardSlot2.health_points > 0) {
        setPlayerActiveCard(playerCardSlot2);
        setPlayerCardSlot2(activePlayerCard);
        let temp = activePlayerCard;
        activePlayerCard = playerCardSlot2;
        playerCardSlot2 = temp;
        swapped = true;
        document.getElementById('player-slot-2-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + username + ` swapped `+ playerCardSlot2.name + ` for ${activePlayerCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        return true;

    } else {
        document.getElementById('player-active-card-icon').classList.add('card-dead');
        alert("Player has no more cards! You lost!");
        battleLog.innerHTML += `<p>` + username + ` has no more cards! You lost!</p>`;
        completeGymBattle(false, gymID);
        disableButtons();
    }
    return false;
}

function checkOpponentGameOver() {
    if (opponentCardSlot1.health_points == 0 && opponentCardSlot2.health_points == 0 && activeOpponentCard.health_points == 0) {
        return true;
    } else {
        return false;
    }
}

function checkPlayerGameOver() {
    if (playerCardSlot1.health_points == 0 && playerCardSlot2.health_points == 0 && activePlayerCard.health_points == 0) {
        return true;
    } else {
        return false;
    }
}

function disableButtons() {
    document.getElementById('player-move-1').disabled = true;
    document.getElementById('player-move-2').disabled = true;
    document.getElementById('player-retreat-1').disabled = true;
    document.getElementById('player-retreat-2').disabled = true;
}

function completeGymBattle(didWin, gymId) {
    const url = `/gym-battle-completed?did_win=${didWin}&gym_id=${gymId}`;
    window.location.href = url;
}