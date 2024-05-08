let balance;
let username = 'your_username'; 

let slotValues = ['🍆', '🍆', '🍑', '🍑', '🍒', '🌮', '🍓'];
let slots = Array.from(document.querySelectorAll('.slot'));
const spinButton = document.getElementById('spin-button');

// pievienoju event listeneri uz spin pogu
spinButton.addEventListener('click', () => {
    // katru reizi kad tiek spiests spin poga, tiek izsaukta funkcija spin
    slots.forEach(slot => {
        slot.textContent = slotValues[Math.floor(Math.random() * slotValues.length)];
    });
    spin(1);

    // pasaucu funkciju getBalance, kas atgriezīs lietotāja atlikumu
    
});

let winningCombinations = [
    // Three-symbol combinations
    [[0, 1, 2], [1, 2, 3], [2, 3, 4], [5, 6, 7], [6, 7, 8], [7, 8, 9], [10, 11, 12], [11, 12, 13], [12, 13, 14]],
    // Four-symbol combinations
    [[0, 1, 2, 3], [1, 2, 3, 4], [5, 6, 7, 8], [6, 7, 8, 9], [10, 11, 12, 13], [11, 12, 13, 14]],
    // Five-symbol combinations
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
];

function flash(message) {
    // nonemt esošo flash ziņojumu, ja tāds ir
    let existingFlashMessage = document.querySelector('.flash');
    if (existingFlashMessage) {
        existingFlashMessage.remove();
    }

    let flashMessage = document.createElement('div');
    flashMessage.textContent = message;
    flashMessage.classList.add('flash');
    document.body.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 5000);
}

function checkResults() {
    let jackpots = [];
    let usedIndexes = new Set();
    let glowingSlots = [];

    // filtressana
    for (let i = winningCombinations.length - 1; i >= 0; i--) {
        for (let combination of winningCombinations[i]) {
            if (combination.every(index => slots[index].textContent === slots[combination[0]].textContent)) {
                
                if (combination.some(index => usedIndexes.has(index))) {
                    continue;
                }

                for (let index of combination) {
                    usedIndexes.add(index);
                }

             
                for (let index of combination) {
                    slots[index].classList.add('glow');
                    glowingSlots.push(slots[index]);  
                }

                jackpots.push(combination.length);
            }
        }
    }

    let resultSound = new Audio(jackpots.length > 0 ? '/static/Win.mp3' : '/static/BRUH.mp3');
    resultSound.play();

    if (jackpots.length > 0) {
        let totalWinningLength = jackpots.reduce((a, b) => a + b, 0);
        flash(`Jackpot! You have ${jackpots.length} winning combinations with a total length of ${totalWinningLength}!`);
    } else {
        flash('Try again!');
    }

    // izsaukšu funkciju, kas noņems glow klasi no slotiem
    setTimeout(() => {
        for (let slot of glowingSlots) {
            slot.classList.remove('glow');
        }
    }, 5000);
}

function spin(amount) {
    // atņemt no atlikuma summu, kas tiek iedota kā argumentu
    balance -= amount;

    let spinSound = new Audio('/static/spin.mp3');  
    spinSound.play();

    let spinInterval = setInterval(() => {
        slots.forEach(slot => {
            slot.textContent = slotValues[Math.floor(Math.random() * slotValues.length)];
        });
    }, 100);

    setTimeout(() => {
        clearInterval(spinInterval);
        checkResults();
    }, 5000);
}

function getBalance(username) {
    fetch(`/balance?username=${username}`)
        .then(response => response.json())
        .then(data => {
            let balance = data.balance;
            
        });
}