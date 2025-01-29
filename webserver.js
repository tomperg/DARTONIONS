// ===============================
// KONSTANTEN & GLOBALE VARIABLEN
// ===============================

// Spielstand und Spieler-Status
let currentPlayer = 1;          // Aktiver Spieler (1 oder 2)
let p1Score = 501;             // Punktestand Spieler 1
let p2Score = 501;             // Punktestand Spieler 2
let currentDarts = 0;          // Anzahl der geworfenen Darts in der aktuellen Runde
let currentMultiplier = 1;     // Aktiver Multiplikator (1 = Single, 2 = Double, 3 = Triple)
let p1Legs = 0;                // Anzahl der gewonnenen Legs von Spieler 1
let p2Legs = 0;                // Anzahl der gewonnenen Legs von Spieler 2

// Spiel-Konfiguration
const maxDartsPerTurn = 3;     // Maximale Anzahl Darts pro Spieler pro Runde
const STARTING_SCORE = 501;    // Startpunktzahl für jeden Spieler

// Neue Datenstruktur für die Würfe
let currentGameThrows = {
    player1: [],  // Jedes Element ist ein Array mit 3 Würfen
    player2: []
};

// Temporärer Speicher für aktuelle Aufnahme
let currentSet = {
    throws: [],
    imuData: {
        angles: [],
        velocities: []
    }
};

// ===============================
// SPIELFELD-GENERIERUNG
// ===============================

function createNumberButtons() {
    const singles = document.getElementById('singles');
    const modifiers = document.getElementById('modifiers');

    // Erstelle Buttons für die Zahlen 1-20
    for(let i = 1; i <= 20; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.id = `single${i}`;
        btn.className = 'number-button';
        btn.onclick = () => updateScore(i * currentMultiplier);
        singles.appendChild(btn);
    }
    
    createBullButton(singles);
    createModifierButtons(modifiers);
}

function createBullButton(container) {
    const bull25 = document.createElement('button');
    bull25.textContent = '25';
    bull25.id = 'single25';
    bull25.className = 'number-button';
    bull25.onclick = () => updateScore(25 * currentMultiplier);
    container.appendChild(bull25);
}

function createModifierButtons(container) {
    const doubleBtn = document.createElement('button');
    doubleBtn.textContent = 'Double';
    doubleBtn.id = 'double';
    doubleBtn.className = 'modifier-button';
    doubleBtn.onclick = () => toggleModifier(2, doubleBtn);
    container.appendChild(doubleBtn);

    const tripleBtn = document.createElement('button');
    tripleBtn.textContent = 'Triple';
    tripleBtn.id = 'triple';
    tripleBtn.className = 'modifier-button';
    tripleBtn.onclick = () => toggleModifier(3, tripleBtn);
    container.appendChild(tripleBtn);
}

// ===============================
// SPIELLOGIK
// ===============================

function toggleModifier(multiplier, button) {
    if (currentMultiplier === multiplier) {
        currentMultiplier = 1;
        button.classList.remove('active');
    } else {
        const modifierButtons = document.querySelectorAll('.modifier-button');
        modifierButtons.forEach(btn => btn.classList.remove('active'));
        currentMultiplier = multiplier;
        button.classList.add('active');
    }
}

function switchPlayer() {
    currentPlayer = currentPlayer === 1 ? 2 : 1;
    document.getElementById('p1').classList.toggle('active');
    document.getElementById('p2').classList.toggle('active');
}

function updateScore(points) {
    if (points === 75) {
        console.error("Triple cannot be applied to 25.");
        alert("Triple cannot be applied to 25.");
        return;
    }

    const scoreElement = currentPlayer === 1 ? 
        document.getElementById('count1') : 
        document.getElementById('count2');
    const currentScore = currentPlayer === 1 ? p1Score : p2Score;
    
    if (currentScore - points >= 0) {
        // Füge den Wurf zum aktuellen Set hinzu
        addThrowToCurrentGame(currentPlayer, points);
        
        // Aktualisiere den Score
        if (currentPlayer === 1) {
            p1Score -= points;
            scoreElement.textContent = p1Score;
        } else {
            p2Score -= points;
            scoreElement.textContent = p2Score;
        }

        scoreElement.classList.add('updating');
        setTimeout(() => {
            scoreElement.classList.remove('updating');
        }, 300);

        if (currentScore - points === 0) {
            handleLegWin();
        }

        currentDarts++;
        if (currentDarts >= maxDartsPerTurn) {
            switchPlayer();
            currentDarts = 0;
        }
    }
}

function handleLegWin() {
    if (currentPlayer === 1) {
        p1Legs++;
        document.getElementById('legsPlayerOne').textContent = p1Legs;
    } else {
        p2Legs++;
        document.getElementById('legsPlayerTwo').textContent = p2Legs;
    }
    alert(`Spieler ${currentPlayer} hat das Leg gewonnen!`);
    resetLeg();
}

// ===============================
// WURF-MANAGEMENT
// ===============================

function addThrowToCurrentGame(playerNumber, points) {
    // Füge den Wurf zum aktuellen Set hinzu
    currentSet.throws.push(points);
    
    // Wenn drei Würfe erreicht sind, speichere das Set
    if (currentSet.throws.length === 3) {
        const playerKey = `player${playerNumber}`;
        const throwSet = {
            throws: [...currentSet.throws],
            total: currentSet.throws.reduce((a, b) => a + b, 0),
            imuData: {
                angles: [...currentSet.imuData.angles],
                velocities: [...currentSet.imuData.velocities]
            },
            timestamp: new Date().toISOString()
        };
        
        currentGameThrows[playerKey].push(throwSet);
        
        // Reset currentSet
        currentSet = {
            throws: [],
            imuData: {
                angles: [],
                velocities: []
            }
        };
    }
    
    // Aktualisiere die Statistiken
    updateStats();
}

// ===============================
// STATISTIK-FUNKTIONEN
// ===============================

function calculatePlayerStats(playerNumber) {
    const sets = currentGameThrows[`player${playerNumber}`];
    
    if (sets.length === 0) return {
        average: 0,
        highest: 0,
        numberOfSets: 0
    };

    const totalPoints = sets.reduce((sum, set) => sum + set.total, 0);
    const highest = Math.max(...sets.map(set => set.total));
    
    return {
        average: totalPoints / sets.length,
        highest: highest,
        numberOfSets: sets.length
    };
}

function updateStats() {
    const p1Stats = calculatePlayerStats(1);
    const p2Stats = calculatePlayerStats(2);
    
    // Update UI
    document.getElementById('p1avg').textContent = p1Stats.average.toFixed(1);
    document.getElementById('p2avg').textContent = p2Stats.average.toFixed(1);
    document.getElementById('p1high').textContent = p1Stats.highest;
    document.getElementById('p2high').textContent = p2Stats.highest;
    document.getElementById('p1games').textContent = p1Stats.numberOfSets;
    document.getElementById('p2games').textContent = p2Stats.numberOfSets;
}

// ===============================
// SPIEL-MANAGEMENT
// ===============================

function resetLeg() {
    p1Score = STARTING_SCORE;
    p2Score = STARTING_SCORE;
    currentDarts = 0;
    document.getElementById('count1').textContent = p1Score;
    document.getElementById('count2').textContent = p2Score;
    
    // Reset auch das aktuelle Set
    currentSet = {
        throws: [],
        imuData: {
            angles: [],
            velocities: []
        }
    };
    currentGameThrows = {
        player1: [],
        player2: []
    };
}

function resetGame() {
    p1Score = STARTING_SCORE;
    p2Score = STARTING_SCORE;
    currentPlayer = 1;
    currentDarts = 0;
    p1Legs = 0;
    p2Legs = 0;
    document.getElementById('count1').textContent = p1Score;
    document.getElementById('count2').textContent = p2Score;
    document.getElementById('legsPlayerOne').textContent = '0';
    document.getElementById('legsPlayerTwo').textContent = '0';
    document.getElementById('p1').classList.add('active');
    document.getElementById('p2').classList.remove('active');
    
    // Reset Sets und Statistiken
    currentSet = {
        throws: [],
        imuData: {
            angles: [],
            velocities: []
        }
    };
    currentGameThrows = {
        player1: [],
        player2: []
    };
    updateStats();
}

// ===============================
// STATISTIK-MODAL
// ===============================

const modal = document.getElementById('statsModal');
const statsBtn = document.getElementById('showStats');
const span = document.getElementsByClassName('close')[0];

statsBtn.onclick = function() {
    updateStats();
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// ===============================
// IMU DATEN MANAGEMENT
// ===============================

function updateIMUData(data) {
    if (currentSet.imuData.angles.length < 3) {
        const velocity = Math.sqrt(
            Math.pow(data.velocity.x, 2) + 
            Math.pow(data.velocity.y, 2) + 
            Math.pow(data.velocity.z, 2)
        );
        
        currentSet.imuData.angles.push(data.last_relative_roll);
        currentSet.imuData.velocities.push(velocity);
    }
}

// ===============================
// EVENT LISTENER
// ===============================

document.getElementById('setupForm').addEventListener('submit', (e) => {
    e.preventDefault();
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';
    
    const p1Name = document.getElementById('player1').value;
    const p2Name = document.getElementById('player2').value;
    document.getElementById('playerOneName').textContent = p1Name;
    document.getElementById('playerTwoName').textContent = p2Name;
});

document.getElementById('nextPlayerButton').addEventListener('click', () => {
    switchPlayer();
    currentDarts = 0;
});

document.getElementById('nextgame').addEventListener('click', resetGame);

// Daten alle 100ms vom Server abrufen
async function fetchData() {
    try {
        const response = await fetch('/data');
        const data = await response.json();
        updateIMUData(data);
    } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
    }
}

// Daten-Abruf starten
setInterval(fetchData, 100);

// ===============================
// SPIEL INITIALISIERUNG
// ===============================

createNumberButtons();