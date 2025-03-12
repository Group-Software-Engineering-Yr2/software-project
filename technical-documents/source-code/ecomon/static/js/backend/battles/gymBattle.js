// Wait for the DOM to be fully loaded before executing the code
// TODO: Commenting all new features
document.addEventListener('DOMContentLoaded', function () {
    // Create and show the coin flip overlay
    createCoinFlipOverlay();

    // Perform the coin flip
    performCoinFlip();

    // Initialize the start variables
    setPlayerActiveCard(activePlayerCard);
    setPlayerCardSlot1(playerCardSlot1);
    setPlayerCardSlot2(playerCardSlot2);
    setOpponentActiveCard(activeOpponentCard);
    setOpponentCardSlot1(opponentCardSlot1);
    setOpponentCardSlot2(opponentCardSlot2);
});

// Initialize the max health variables for player and opponent cards
let playerCardsMaxHealth;
let maxOpponentHealth;

// Function to create the coin flip overlay
function createCoinFlipOverlay() {
    // Create overlay div
    const overlay = document.createElement('div');
    overlay.id = 'coin-flip-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    overlay.style.display = 'flex';
    overlay.style.flexDirection = 'column';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = '1000';

    // Create text for coin flip
    const text = document.createElement('div');
    text.id = 'coin-flip-text';
    text.textContent = 'Flipping coin to decide who goes first...';
    text.style.color = 'white';
    text.style.fontSize = '24px';
    text.style.marginBottom = '30px';
    text.style.fontFamily = 'Arial, sans-serif';
    text.style.fontWeight = 'bold';

    // Create coin container
    const coinContainer = document.createElement('div');
    coinContainer.id = 'coin-container';
    coinContainer.style.width = '150px';
    coinContainer.style.height = '150px';
    coinContainer.style.position = 'relative';
    coinContainer.style.perspective = '1000px';
    coinContainer.style.marginBottom = '30px'; // Add margin below coin

    // Create the coin
    const coin = document.createElement('div');
    coin.id = 'coin';
    coin.style.width = '100%';
    coin.style.height = '100%';
    coin.style.position = 'relative';
    coin.style.transformStyle = 'preserve-3d';
    coin.style.transition = 'transform 1s ease-in';

    // Create heads side
    const heads = document.createElement('div');
    heads.className = 'coin-side heads';
    heads.style.width = '100%';
    heads.style.height = '100%';
    heads.style.position = 'absolute';
    heads.style.backfaceVisibility = 'hidden';
    heads.style.borderRadius = '50%';
    heads.style.backgroundColor = '#84C44C';
    heads.style.display = 'flex';
    heads.style.justifyContent = 'center';
    heads.style.alignItems = 'center';
    heads.style.fontSize = '24px';
    heads.style.fontWeight = 'bold';
    heads.style.color = 'white';
    heads.textContent = username;

    // Create tails side
    const tails = document.createElement('div');
    tails.className = 'coin-side tails';
    tails.style.width = '100%';
    tails.style.height = '100%';
    tails.style.position = 'absolute';
    tails.style.backfaceVisibility = 'hidden';
    tails.style.borderRadius = '50%';
    tails.style.backgroundColor = '#FF0000';
    tails.style.transform = 'rotateY(180deg)';
    tails.style.display = 'flex';
    tails.style.justifyContent = 'center';
    tails.style.alignItems = 'center';
    tails.style.fontSize = '24px';
    tails.style.fontWeight = 'bold';
    tails.style.color = 'white';
    tails.textContent = opponent;

    // Create team info container
    const teamInfoContainer = document.createElement('div');
    teamInfoContainer.id = 'team-info-container';
    teamInfoContainer.style.display = 'flex';
    teamInfoContainer.style.justifyContent = 'space-between';
    teamInfoContainer.style.width = '80%';
    teamInfoContainer.style.maxWidth = '800px';
    teamInfoContainer.style.color = 'white';
    teamInfoContainer.style.fontFamily = 'Arial, sans-serif';

    // Create user team info
    const userTeamInfo = document.createElement('div');
    userTeamInfo.className = 'team-info';
    userTeamInfo.style.padding = '15px';
    userTeamInfo.style.backgroundColor = 'rgba(132, 196, 76, 0.3)';
    userTeamInfo.style.borderRadius = '8px';
    userTeamInfo.style.width = '45%';
    userTeamInfo.style.textAlign = 'center';

    const userTeamTitle = document.createElement('h3');
    userTeamTitle.textContent = username + "'s Team";
    userTeamTitle.style.color = '#84C44C';
    userTeamTitle.style.marginTop = '0';
    userTeamTitle.style.marginBottom = '10px';

    const userTeamBenefits = document.createElement('p');
    if (userTeam === "Recycle") {
        userTeamBenefits.textContent = 'Recycle Team Benefits: Recycle cards deal +10 damage on all moves';
        userTeamBenefits.style.margin = '0';
    } else if (userTeam === "Reduce") {
        userTeamBenefits.textContent = 'Reduce Team Benefits: Player takes -5 damage from all moves';
        userTeamBenefits.style.margin = '0';
    } else if (userTeam === "Reuse") {
        userTeamBenefits.textContent = 'Reuse Team Benefits: Players cards have increased use count';
        userTeamBenefits.style.margin = '0';
    }
    userTeamInfo.appendChild(userTeamTitle);
    userTeamInfo.appendChild(userTeamBenefits);

    // Create opponent team info
    const opponentTeamInfo = document.createElement('div');
    opponentTeamInfo.className = 'team-info';
    opponentTeamInfo.style.padding = '15px';
    opponentTeamInfo.style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
    opponentTeamInfo.style.borderRadius = '8px';
    opponentTeamInfo.style.width = '45%';
    opponentTeamInfo.style.textAlign = 'center';

    const opponentTeamTitle = document.createElement('h3');
    opponentTeamTitle.textContent = opponent + "'s Team";
    opponentTeamTitle.style.color = '#FF0000';
    opponentTeamTitle.style.marginTop = '0';
    opponentTeamTitle.style.marginBottom = '10px';

    const opponentTeamBenefits = document.createElement('p');
    if (opponentTeam === "Recycle") {
        opponentTeamBenefits.textContent = 'Recycle Team Benefits: Recycle cards deal +10 damage on all moves';
    } else if (opponentTeam === "Reduce") {
        opponentTeamBenefits.textContent = 'Reduce Team Benefits: Opponent takes -5 damage from all moves';
    } else if (opponentTeam === "Reuse") {
        opponentTeamBenefits.textContent = 'Reuse Team Benefits: Opponents cards have increased use count';
    } else {
        opponentTeamBenefits.textContent = 'Fossil Fuel Team Benefits: No team benefits';
    }
    opponentTeamBenefits.style.margin = '0';
    opponentTeamInfo.appendChild(opponentTeamTitle);
    opponentTeamInfo.appendChild(opponentTeamBenefits);

    // Add team info to container
    teamInfoContainer.appendChild(userTeamInfo);
    teamInfoContainer.appendChild(opponentTeamInfo);

    // Initially hide team info
    teamInfoContainer.style.opacity = '0';
    teamInfoContainer.style.transition = 'opacity 0.5s ease';

    // Assemble the elements
    coin.appendChild(heads);
    coin.appendChild(tails);
    coinContainer.appendChild(coin);
    overlay.appendChild(text);
    overlay.appendChild(coinContainer);
    overlay.appendChild(teamInfoContainer);
    document.body.appendChild(overlay);
}

function performCoinFlip() {
    const coin = document.getElementById('coin');
    const text = document.getElementById('coin-flip-text');
    const overlay = document.getElementById('coin-flip-overlay');
    const teamInfo = document.getElementById('team-info-container');

    // Ensure coin starts at 0 rotation
    coin.style.transform = "rotateY(0deg)";

    // Force a reflow before applying the animation
    setTimeout(() => {
        // Random number of rotations (5 to 10)
        const rotations = 5 + Math.floor(Math.random() * 5);
        const isHeads = Math.random() < 0.5;
        const finalRotation = rotations * 360 + (isHeads ? 0 : 180);

        // Apply the rotation to the coin
        coin.style.transition = "transform 1s ease-in-out";
        coin.style.transform = `rotateY(${finalRotation}deg)`;

        setTimeout(() => {
            text.textContent = isHeads ? `${username} goes first!` : `${opponent} goes first!`;
            isPlayerTurn = isHeads;

            // Show team information
            teamInfo.style.opacity = '1';

            // Increased delay before game starts (4 seconds instead of 1.5)
            setTimeout(() => {
                overlay.style.opacity = '0';
                overlay.style.transition = 'opacity 0.8s ease';

                // Increased delay for fade out (1 second instead of 0.5)
                setTimeout(() => {
                    document.body.removeChild(overlay);
                    startGame();
                }, 1000);
            }, 4000);
        }, 1000);
    }, 50); // Tiny delay to trigger reflow
}

// Function to start the game after the coin flip
function startGame() {
    // Initialize the start variables and rendering the cards
    setPlayerActiveCard(activePlayerCard);
    setPlayerCardSlot1(playerCardSlot1);
    setPlayerCardSlot2(playerCardSlot2);
    setOpponentActiveCard(activeOpponentCard);
    setOpponentCardSlot1(opponentCardSlot1);
    setOpponentCardSlot2(opponentCardSlot2);

    // Initialize the max health points for the player's cards
    let maxActivePlayerCardHealth = activePlayerCard.health_points;
    let maxPlayerCardSlot1Health = playerCardSlot1.health_points;
    let maxPlayerCardSlot2Health = playerCardSlot2.health_points;

    playerCardsMaxHealth = {
        activePlayerCard: maxActivePlayerCardHealth,
        playerCardSlot1: maxPlayerCardSlot1Health,
        playerCardSlot2: maxPlayerCardSlot2Health
    }

    // Initialize battle log
    let battleLog = document.querySelector('.battle-log');
    battleLog.innerHTML += `<p>Coin flip result: ${isPlayerTurn ? username : opponent} goes first!</p>`;
    battleLog.scrollTop = battleLog.scrollHeight;

    // If opponent goes first, start their turn
    if (!isPlayerTurn) {
        setTimeout(() => {
            handleOpponentTurn();
        }, 1000);
    }

    // Add event listeners for button clicks on the HTML page
    // Player move 1
    document.getElementById('player-move-1').addEventListener('click', function () {
        // Check if it is the player's turn
        if (isPlayerTurn) {
            // Handle player's turn if the first move button is clicked
            handlePlayerTurn(1);
        }
    });

    // Player move 2
    document.getElementById('player-move-2').addEventListener('click', function () {
        // Check if it is the player's turn
        if (isPlayerTurn) {
            // Handle player's turn if the first move button is clicked
            handlePlayerTurn(2);
        }
    });

    // Player retreat 1
    document.getElementById('player-retreat-1').addEventListener('click', function () {
        // Check if it is the player's turn
        if (isPlayerTurn) {
            // Check if the card in slot 1 is alive, if true, process the retreat
            if (playerCardSlot1.health_points > 0) {
                handlePlayerTurn(3);
                setPlayerActiveCard(playerCardSlot1);
                setPlayerCardSlot1(activePlayerCard);
                let tempMax = playerCardsMaxHealth.activePlayerCard;
                playerCardsMaxHealth.activePlayerCard = playerCardsMaxHealth.playerCardSlot1;
                playerCardsMaxHealth.playerCardSlot1 = tempMax;
                let temp = activePlayerCard;
                activePlayerCard = playerCardSlot1;
                playerCardSlot1 = temp;
            } else {
                alert("Unable to retreat, the card in Slot 1 is dead!");
            }
        }
    });

    // Player retreat 2
    document.getElementById('player-retreat-2').addEventListener('click', function () {
        // Check if it is the player's turn
        if (isPlayerTurn) {
            // Check if the card in slot 2 is alive, if true, process the retreat
            if (playerCardSlot2.health_points > 0) {
                handlePlayerTurn(4);
                setPlayerActiveCard(playerCardSlot2);
                setPlayerCardSlot2(activePlayerCard);
                let tempMax = playerCardsMaxHealth.activePlayerCard;
                playerCardsMaxHealth.activePlayerCard = playerCardsMaxHealth.playerCardSlot2;
                playerCardsMaxHealth.playerCardSlot2 = tempMax;
                let temp = activePlayerCard;
                activePlayerCard = playerCardSlot2;
                playerCardSlot2 = temp;
            } else {
                alert("Unable to retreat, the card in Slot 2 is dead!");
            }
        }
    });
}

// The rest of your existing functions remain unchanged
function setPlayerActiveCard(card) {
    document.getElementById('player-active-card-icon').src = card.image;
    document.getElementById('player-hp').textContent = `HP: ${card.health_points}`;
    document.getElementById('player-active-card-name').textContent = card.name;
    document.getElementById('player-move-1').textContent = card.ability_name_1 + ": " + card.ability_power_1 + " Damage";
    // Check if the second sustainAbility is a damage move only
    if (card.ability_power_2 > 0 && card.ability_self_power_2 == 0) {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": " + card.ability_power_2 + " Damage";
        // Check if the second sustainAbility is a heal and damage move
    } else if (card.ability_power_2 > 0 && card.ability_self_power_2 > 0) {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": " + card.ability_power_2 + " Damage and +" + card.ability_self_power_2 + " Health";
        // Otherwise its a heal move only
    } else {
        document.getElementById('player-move-2').textContent = card.ability_name_2 + ": +" + card.ability_self_power_2 + " Health";
    }
    document.getElementById('player-retreat-1').textContent = "Retreat " + card.name + " for Bench Card 1";
    document.getElementById('player-retreat-2').textContent = "Retreat " + card.name + " for Bench Card 2";
}

//Function to set the player's card in slot 1 on the HTML page
function setPlayerCardSlot1(card) {
    document.getElementById('player-slot-1-icon').src = card.image;
}

//Function to set the player's card in slot 2 on the HTML page
function setPlayerCardSlot2(card) {
    document.getElementById('player-slot-2-icon').src = card.image;
}

//Function to set the opponent's active card on the HTML page
function setOpponentActiveCard(card) {
    // Set the opponent's active card on the HTML page and initialize the maxOpponentHealth
    maxOpponentHealth = card.health_points;
    document.getElementById('opponent-active-card-icon').src = card.image;
    document.getElementById('opponent-hp').textContent = `HP: ${card.health_points}`;
    document.getElementById('opponent-active-card-name').textContent = card.name;
}

//Function to set the opponent's card in slot 1 on the HTML page
function setOpponentCardSlot1(card) {
    document.getElementById('opponent-slot-1-icon').src = card.image;
}

//Function to set the opponent's card in slot 2 on the HTML page
function setOpponentCardSlot2(card) {
    document.getElementById('opponent-slot-2-icon').src = card.image;
}

// Animation Functions
function animateAttack(attackingCardElement, receivingCardElement, damage, isHeal = false) {
    // Get the card elements by their containers
    const attackingCard = attackingCardElement || document.querySelector('.gym-battle-player-active .active-card');
    const receivingCard = receivingCardElement || document.querySelector('.gym-battle-opponent-active .active-card');

    // Add a class to trigger the animation
    attackingCard.classList.add('card-attacking');

    // If it's a damage move, also animate the receiving card
    if (!isHeal && damage > 0) {
        receivingCard.classList.add('card-receiving-damage');

        // Create and append damage number element
        const damageElement = document.createElement('div');
        damageElement.className = 'damage-number';
        damageElement.textContent = `-${damage}`;
        // document.querySelector('.gym-battle-area').appendChild(damageElement);
        document.querySelector('.battle-content').appendChild(damageElement);

        // Position the damage number near the receiving card
        const cardRect = receivingCard.getBoundingClientRect();
        damageElement.style.left = `${cardRect.left + cardRect.width / 2}px`;
        damageElement.style.top = `${cardRect.top + cardRect.height / 2}px`;

        // Remove damage number after animation completes
        setTimeout(() => {
            damageElement.remove();
        }, 1500);
    }

    // If it's a heal move
    if (isHeal) {
        attackingCard.classList.add('card-healing');

        // Create and append heal number element
        const healElement = document.createElement('div');
        healElement.className = 'heal-number';
        healElement.textContent = `+${damage}`;
        document.querySelector('.battle-content').appendChild(healElement);

        // Position the heal number near the healing card
        const cardRect = attackingCard.getBoundingClientRect();
        healElement.style.left = `${cardRect.left + cardRect.width / 2}px`;
        healElement.style.top = `${cardRect.top + cardRect.height / 2}px`;

        // Remove heal number after animation completes
        setTimeout(() => {
            healElement.remove();
        }, 1500);
    }

    // Remove animation classes after they complete
    setTimeout(() => {
        attackingCard.classList.remove('card-attacking');
        if (!isHeal) {
            receivingCard.classList.remove('card-receiving-damage');
        }
        attackingCard.classList.remove('card-healing');
    }, 1000);
}

// Flash the battle log when updated
function flashBattleLog() {
    const battleLog = document.querySelector('.battle-log');
    battleLog.classList.add('battle-log-flash');

    setTimeout(() => {
        battleLog.classList.remove('battle-log-flash');
    }, 1000);
}

// Modified handlePlayerTurn function with animations
function handlePlayerTurn(moveChoice) {
    // Initialize variables, change to opponents turn after player's turn, and set the battle log
    isPlayerTurn = false;
    let battleLog = document.querySelector('.battle-log');
    const playerCardElement = document.querySelector('.gym-battle-player-active .active-card');
    const opponentCardElement = document.querySelector('.gym-battle-opponent-active .active-card');

    // Handles First Move Button Click (First sustainAbility)
    if (moveChoice === 1) {
        // Trigger attack animation before updating HP
        animateAttack(playerCardElement, opponentCardElement, activePlayerCard.ability_power_1);

        // Continue with your existing logic after a slight delay to let animation start
        setTimeout(() => {
            let result = activeOpponentCard.health_points - activePlayerCard.ability_power_1;
            // If the opponent's health points are less than or equal to 0 after the players move
            if (result <= 0) {
                result = 0;
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_1 + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();

                setTimeout(() => {
                    battleLog.innerHTML += `<p>` + opponent + `'s ` + activeOpponentCard.name + ` fainted!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();
                    // Check if the opponent has any more cards
                    checkOpponentDeadCard();
                }, 1000);
            } else {
                activeOpponentCard.health_points = result;
                document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_1 + ` for ${activePlayerCard.ability_power_1} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();
            }
        }, 300); // Small delay to let animation start before updating HP
    }
    // Handles Second Move Button Click (Second sustainAbility)
    else if (moveChoice === 2) {
        // If the second sustainAbility is a heal move only and player's health points are already maxed out
        if ((activePlayerCard.health_points === playerCardsMaxHealth.activePlayerCard) && (activePlayerCard.ability_self_power_2 > 0 && activePlayerCard.ability_power_2 === 0)) {
            alert("Your health points are already maxed out! Choose a different move!");
            isPlayerTurn = true;
            return;
        }

        // If the second sustainAbility is a damage move only
        if (activePlayerCard.ability_power_2 > 0 && activePlayerCard.ability_self_power_2 == 0) {
            // Trigger attack animation
            animateAttack(playerCardElement, opponentCardElement, activePlayerCard.ability_power_2);

            setTimeout(() => {
                let result = activeOpponentCard.health_points - activePlayerCard.ability_power_2;
                // If the opponent's health points are less than or equal to 0
                if (result <= 0) {
                    result = 0;
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                    // Add to battle log
                    battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();

                    setTimeout(() => {
                        battleLog.innerHTML += `<p>` + opponent + `'s ` + activeOpponentCard.name + ` fainted!</p>`;
                        battleLog.scrollTop = battleLog.scrollHeight;
                        flashBattleLog();
                        // Check if the opponent has any more cards
                        checkOpponentDeadCard();
                    }, 1000);
                } else {
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                    // Add to battle log
                    battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();
                }
            }, 300);
        }
        // If the second sustainAbility is a heal and damage move
        else if (activePlayerCard.ability_power_2 > 0 && activePlayerCard.ability_self_power_2 > 0) {
            // First do the damage animation
            animateAttack(playerCardElement, opponentCardElement, activePlayerCard.ability_power_2);

            setTimeout(() => {
                let result = activeOpponentCard.health_points - activePlayerCard.ability_power_2;
                // Process damage part first
                if (result <= 0) {
                    result = 0;
                    // Update opponent's health
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                    // Now do the heal animation after damage is done
                    setTimeout(() => {
                        let selfResult = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
                        let message = "";
                        if (selfResult > playerCardsMaxHealth.activePlayerCard) {
                            selfResult = playerCardsMaxHealth.activePlayerCard;
                            message = ` and healed ${playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points} health!`;
                            // Trigger heal animation
                            animateAttack(playerCardElement, playerCardElement, playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points, true);
                            activePlayerCard.health_points = result;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                            battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage` + message + `</p>`;
                        } else {
                            // Trigger heal animation
                            animateAttack(playerCardElement, playerCardElement, activePlayerCard.ability_self_power_2, true);
                            activePlayerCard.health_points = selfResult;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                            battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage and healed ${activePlayerCard.ability_self_power_2} health!</p>`;
                        }

                        // Update player's health after a slight delay
                        setTimeout(() => {
                            activePlayerCard.health_points = selfResult;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                            setTimeout(() => {
                                battleLog.innerHTML += `<p>` + opponent + `'s ` + activeOpponentCard.name + ` fainted!</p>`;
                                battleLog.scrollTop = battleLog.scrollHeight;
                                flashBattleLog();
                                // Check if the opponent has any more cards
                                checkOpponentDeadCard();
                            }, 800);
                        }, 300);
                    }, 800);
                } else {
                    // Process regular damage
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                    // Now do the heal animation after damage is done
                    setTimeout(() => {
                        let selfResult = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
                        let message = "";
                        if (selfResult > playerCardsMaxHealth.activePlayerCard) {
                            selfResult = playerCardsMaxHealth.activePlayerCard;
                            message = ` and healed ${playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points} health!`;
                            // Trigger heal animation
                            animateAttack(playerCardElement, playerCardElement, playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points, true);
                            activePlayerCard.health_points = result;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                            battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage` + message + `</p>`;
                        } else {
                            // Trigger heal animation
                            animateAttack(playerCardElement, playerCardElement, activePlayerCard.ability_self_power_2, true);
                            activePlayerCard.health_points = selfResult;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                            battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` for ${activePlayerCard.ability_power_2} damage and healed ${activePlayerCard.ability_self_power_2} health!</p>`;
                        }

                        // Update player's health after a slight delay
                        setTimeout(() => {
                            activePlayerCard.health_points = selfResult;
                            document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                        }, 300);
                    }, 800);
                }
            }, 300);
        }
        // If the second sustainAbility is a heal move only
        else {
            setTimeout(() => {
                // Update the health points for the player
                let result = activePlayerCard.health_points + activePlayerCard.ability_self_power_2;
                let message = "";
                if (result > playerCardsMaxHealth.activePlayerCard) {
                    result = playerCardsMaxHealth.activePlayerCard;
                    message = ` and healed ${playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points} health!`;
                    // Trigger heal animation
                    animateAttack(playerCardElement, playerCardElement, playerCardsMaxHealth.activePlayerCard - activePlayerCard.health_points, true);
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                    battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + message + `</p>`;
                } else {
                    // Trigger heal animation
                    animateAttack(playerCardElement, playerCardElement, activePlayerCard.ability_self_power_2, true);
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;
                    battleLog.innerHTML += `<p>` + username + ` used ` + activePlayerCard.ability_name_2 + ` to heal ${activePlayerCard.ability_self_power_2} health!</p>`;
                }
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();
            }, 300);
        }
    }
    // Handle retreat animations
    else if (moveChoice === 3) {
        // Handles retreat action for slot 1
        battleLog.innerHTML += `<p>` + username + ` retreated ` + activePlayerCard.name + ` for ` + playerCardSlot1.name + `!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        flashBattleLog();
    }
    else if (moveChoice === 4) {
        // Handles retreat action for slot 2
        battleLog.innerHTML += `<p>` + username + ` retreated ` + activePlayerCard.name + ` for ` + playerCardSlot2.name + `!</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
        flashBattleLog();
    }

    // Check game over & start opponent's turn after a longer delay to allow animations to complete
    if (!checkOpponentGameOver()) {
        if (moveChoice === 3 || moveChoice === 4) {
            setTimeout(() => {
                handleOpponentTurn();
            }, 1000); // Decreased delay as there is a shorter retreat animation
        } else {
            setTimeout(() => {
                handleOpponentTurn();
            }, 2500); // Increased delay to account for animations
        }
    } else {
        isPlayerTurn = true;
    }
}

// Handle opponent's turn
function handleOpponentTurn() {
    // Disable player buttons during opponent's turn
    disablePlayerButtons();
    // Initialize battle log and choose a random move for the opponent
    let battleLog = document.querySelector('.battle-log');
    const moveChoice = Math.random() < 0.5 ? 1 : 2;
    const playerCardElement = document.querySelector('.gym-battle-player-active .active-card');
    const opponentCardElement = document.querySelector('.gym-battle-opponent-active .active-card');

    // If the opponent randomly chooses the first move
    if (moveChoice === 1) {
        // Trigger attack animation before updating HP
        animateAttack(opponentCardElement, playerCardElement, activeOpponentCard.ability_power_1);

        // Continue with your existing logic after a slight delay to let animation start
        setTimeout(() => {
            let result = activePlayerCard.health_points - activeOpponentCard.ability_power_1;
            // If the player's health points are less than or equal to 0 after the opponent's move, set the health points to 0 and update the HTML
            if (result <= 0) {
                result = 0;
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_1 + ` for ${activeOpponentCard.ability_power_1} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();

                setTimeout(() => {
                    battleLog.innerHTML += `<p>` + username + `'s ` + activePlayerCard.name + ` fainted!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();
                    // Check if the player has any more cards, if not, the opponent wins
                    checkPlayerDeadCard();
                }, 1000);
            } else {
                activePlayerCard.health_points = result;
                document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                // Add to battle log
                battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_1 + ` for ${activeOpponentCard.ability_power_1} damage!</p>`;
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();
            }
        }, 300); // Small delay to let animation start before updating HP

        // If the opponent randomly chooses the second move
    } else if (moveChoice === 2) {
        // If the second sustainAbility is a heal move only and the opponent's health points are already maxed out, make the AI opponent choose a different move
        if ((activeOpponentCard.health_points === maxOpponentHealth) && (activeOpponentCard.ability_self_power_2 > 0 && activeOpponentCard.ability_power_2 === 0)) {
            isPlayerTurn = false;
            handleOpponentTurn();
            return;
        }

        // If the second sustainAbility is a damage move only
        if (activeOpponentCard.ability_power_2 > 0 && activeOpponentCard.ability_self_power_2 == 0) {
            // Trigger attack animation
            animateAttack(opponentCardElement, playerCardElement, activeOpponentCard.ability_power_2);

            setTimeout(() => {
                let result = activePlayerCard.health_points - activeOpponentCard.ability_power_2;
                // If the player's health points are less than or equal to 0
                if (result <= 0) {
                    result = 0;
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                    // Add to battle log
                    battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();

                    setTimeout(() => {
                        battleLog.innerHTML += `<p>` + username + `'s ` + activePlayerCard.name + ` fainted!</p>`;
                        battleLog.scrollTop = battleLog.scrollHeight;
                        flashBattleLog();
                        // Check if the player has any more cards
                        checkPlayerDeadCard();
                    }, 1000);
                } else {
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                    // Add to battle log
                    battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage!</p>`;
                    battleLog.scrollTop = battleLog.scrollHeight;
                    flashBattleLog();
                }
            }, 300);
        }
        // If the second sustainAbility is a heal and damage move
        else if (activeOpponentCard.ability_power_2 > 0 && activeOpponentCard.ability_self_power_2 > 0) {
            // First do the damage animation
            animateAttack(opponentCardElement, playerCardElement, activeOpponentCard.ability_power_2);

            setTimeout(() => {
                let result = activePlayerCard.health_points - activeOpponentCard.ability_power_2;
                // Process damage part first
                if (result <= 0) {
                    result = 0;
                    // Update player's health
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                    // Now do the heal animation after damage is done
                    setTimeout(() => {
                        let selfResult = activeOpponentCard.health_points + activeOpponentCard.ability_self_power_2;
                        let message = "";
                        if (selfResult > maxOpponentHealth) {
                            selfResult = maxOpponentHealth;
                            message = ` and healed ${maxOpponentHealth - activeOpponentCard.health_points} health!`;
                            // Trigger heal animation
                            animateAttack(opponentCardElement, opponentCardElement, maxOpponentHealth - activeOpponentCard.health_points, true);
                            activeOpponentCard.health_points = result;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                            battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage` + message + `</p>`;
                        } else {
                            // Trigger heal animation
                            animateAttack(opponentCardElement, opponentCardElement, activeOpponentCard.ability_self_power_2, true);
                            activeOpponentCard.health_points = selfResult;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                            battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage and healed ${activeOpponentCard.ability_self_power_2} health!</p>`;
                        }

                        // Update opponent's health after a slight delay
                        setTimeout(() => {
                            activeOpponentCard.health_points = selfResult;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;

                            setTimeout(() => {
                                battleLog.innerHTML += `<p>` + username + `'s ` + activePlayerCard.name + ` fainted!</p>`;
                                battleLog.scrollTop = battleLog.scrollHeight;
                                flashBattleLog();
                                // Check if the opponent has any more cards
                                checkPlayerDeadCard();
                            }, 800);
                        }, 300);
                    }, 800);
                } else {
                    // Process regular damage
                    activePlayerCard.health_points = result;
                    document.getElementById('player-hp').textContent = `HP: ${activePlayerCard.health_points}`;

                    // Now do the heal animation after damage is done
                    setTimeout(() => {
                        let selfResult = activeOpponentCard.health_points + activeOpponentCard.ability_self_power_2;
                        let message = "";
                        if (selfResult > maxOpponentHealth) {
                            selfResult = maxOpponentHealth;
                            message = ` and healed ${maxOpponentHealth - activeOpponentCard.health_points} health!`;
                            // Trigger heal animation
                            animateAttack(opponentCardElement, opponentCardElement, maxOpponentHealth - activeOpponentCard.health_points, true);
                            activeOpponentCard.health_points = result;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                            battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage` + message + `</p>`;
                        } else {
                            // Trigger heal animation
                            animateAttack(opponentCardElement, opponentCardElement, activeOpponentCard.ability_self_power_2, true);
                            activeOpponentCard.health_points = selfResult;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                            battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` for ${activeOpponentCard.ability_power_2} damage and healed ${activeOpponentCard.ability_self_power_2} health!</p>`;
                        }

                        // Update opponent's health after a slight delay
                        setTimeout(() => {
                            activeOpponentCard.health_points = selfResult;
                            document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                        }, 300);
                    }, 800);
                }
            }, 300);

            // If the second sustainAbility is a heal move only
        } else {
            setTimeout(() => {
                // Update the health points for the opponent
                let result = activeOpponentCard.health_points + activeOpponentCard.ability_self_power_2;
                let message = "";
                if (result > maxOpponentHealth) {
                    result = maxOpponentHealth;
                    message = ` and healed ${maxOpponentHealth - activeOpponentCard.health_points} health!`;
                    // Trigger heal animation
                    animateAttack(opponentCardElement, opponentCardElement, maxOpponentHealth - activeOpponentCard.health_points, true);
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                    battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + message + `</p>`;
                } else {
                    // Trigger heal animation
                    animateAttack(opponentCardElement, opponentCardElement, activeOpponentCard.ability_self_power_2, true);
                    activeOpponentCard.health_points = result;
                    document.getElementById('opponent-hp').textContent = `HP: ${activeOpponentCard.health_points}`;
                    battleLog.innerHTML += `<p>` + opponent + ` used ` + activeOpponentCard.ability_name_2 + ` to heal ${activeOpponentCard.ability_self_power_2} health!</p>`;
                }
                battleLog.scrollTop = battleLog.scrollHeight;
                flashBattleLog();
            }, 300);
        }
    }

    // Check for game over and set back to player's turn
    if (!checkPlayerGameOver()) {
        // Enable player buttons after opponent's turn
        setTimeout(() => {
            enableButtons();
        }, 1500);
        isPlayerTurn = true;
    } else {
        isPlayerTurn = false;
        setTimeout(() => {
            handleOpponentTurn();
        }, 2500); // Increased delay to account for animations
    }
}

// Function to check if the opponent's active card is dead, if so, swap with first slot card, if that
// card is dead, swap with second slot card, if that card is dead, all cards are dead and the player wins
function checkOpponentDeadCard() {
    // Initialize battle log
    let battleLog = document.querySelector('.battle-log');
    // Checks if the opponent's card in slot 1 is alive, if true, process the swap
    if (opponentCardSlot1.health_points > 0) {
        setOpponentActiveCard(opponentCardSlot1);
        setOpponentCardSlot1(activeOpponentCard);
        let temp = activeOpponentCard
        activeOpponentCard = opponentCardSlot1;
        opponentCardSlot1 = temp;
        document.getElementById('opponent-slot-1-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + opponent + ` swapped ` + opponentCardSlot1.name + ` for ${activeOpponentCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;

        // Checks if the opponent's card in slot 2 is alive, if true, process the swap
    } else if (opponentCardSlot2.health_points > 0) {
        setOpponentActiveCard(opponentCardSlot2);
        setOpponentCardSlot2(activeOpponentCard);
        let temp = activeOpponentCard;
        activeOpponentCard = opponentCardSlot2;
        opponentCardSlot2 = temp;
        document.getElementById('opponent-slot-2-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + opponent + ` swapped ` + opponentCardSlot2.name + ` for ${activeOpponentCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;

        // If both cards are dead, the player wins    
    } else {
        document.getElementById('opponent-active-card-icon').classList.add('card-dead');
        alert("Opponent has no more cards! You win!");
        battleLog.innerHTML += `<p>` + opponent + ` has no more cards! You win!</p>`;
        completeGymBattle(true, gymID);
        disablePlayerButtons();
    }
}

// Function to check if the player's active card is dead, if so, swap with first slot card, if that
// card is dead, swap with second slot card, if that card is dead, all cards are dead and the player loses
function checkPlayerDeadCard() {
    // Initialize battle log
    let battleLog = document.querySelector('.battle-log');
    // Checks if the player's card in slot 1 is alive, if true, process the swap
    if (playerCardSlot1.health_points > 0) {
        setPlayerActiveCard(playerCardSlot1);
        setPlayerCardSlot1(activePlayerCard);
        let tempMax = playerCardsMaxHealth.activePlayerCard;
        playerCardsMaxHealth.activePlayerCard = playerCardsMaxHealth.playerCardSlot1;
        playerCardsMaxHealth.playerCardSlot1 = tempMax;
        let temp = activePlayerCard
        activePlayerCard = playerCardSlot1;
        playerCardSlot1 = temp;
        document.getElementById('player-slot-1-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + username + ` swapped ` + playerCardSlot1.name + ` for ${activePlayerCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;

        // Checks if the player's card in slot 2 is alive, if true, process the swap    
    } else if (playerCardSlot2.health_points > 0) {
        setPlayerActiveCard(playerCardSlot2);
        setPlayerCardSlot2(activePlayerCard);
        let tempMax = playerCardsMaxHealth.activePlayerCard;
        playerCardsMaxHealth.activePlayerCard = playerCardsMaxHealth.playerCardSlot2;
        playerCardsMaxHealth.playerCardSlot2 = tempMax;
        let temp = activePlayerCard;
        activePlayerCard = playerCardSlot2;
        playerCardSlot2 = temp;
        document.getElementById('player-slot-2-icon').classList.add('card-dead');
        battleLog.innerHTML += `<p>` + username + ` swapped ` + playerCardSlot2.name + ` for ${activePlayerCard.name}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;

        // If both cards are dead, the player loses    
    } else {
        document.getElementById('player-active-card-icon').classList.add('card-dead');
        alert("Player has no more cards! You lost!");
        battleLog.innerHTML += `<p>` + username + ` has no more cards! You lost!</p>`;
        completeGymBattle(false, gymID);
        disablePlayerButtons();
    }
}

// Function to check if the opponent has no more cards, if so, the player wins
function checkOpponentGameOver() {
    if (opponentCardSlot1.health_points == 0 && opponentCardSlot2.health_points == 0 && activeOpponentCard.health_points == 0) {
        return true;
    } else {
        return false;
    }
}

// Function to check if the player has no more cards, if so, the player loses
function checkPlayerGameOver() {
    if (playerCardSlot1.health_points == 0 && playerCardSlot2.health_points == 0 && activePlayerCard.health_points == 0) {
        return true;
    } else {
        return false;
    }
}

// Function to complete the gym battle and redirect to the gym battle completed page
function completeGymBattle(didWin, gymId) {
    const url = `/gym-battle-completed?did_win=${didWin}&gym_id=${gymId}`;
    window.location.href = url;
}

// Function to disable all buttons during the opponent's turn
function disablePlayerButtons() {
    document.getElementById('player-move-1').disabled = true;
    document.getElementById('player-move-2').disabled = true;
    document.getElementById('player-retreat-1').disabled = true;
    document.getElementById('player-retreat-2').disabled = true;
    document.getElementById('see-bench-cards').disabled = true;
}

// Function to enable all buttons during the player's turn
function enableButtons() {
    document.getElementById('player-move-1').disabled = false;
    document.getElementById('player-move-2').disabled = false;
    document.getElementById('player-retreat-1').disabled = false;
    document.getElementById('player-retreat-2').disabled = false;
    document.getElementById('see-bench-cards').disabled = false;
}