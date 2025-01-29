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

// Datenstrukturen für die Würfe
let currentGameThrows = {
    player1: [], // Jedes Element ist ein Set von 3 Würfen
    player2: []
};

// Temporärer Speicher für die aktuelle Aufnahme
let currentSet = {
    throws: [],           // Punktzahlen
    imuData: {
        angles: [],       // Winkel der Würfe
        velocities: []    // Geschwindigkeiten der Würfe
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

// In der handleLegWin Funktion, direkt vor dem Reset:
function handleLegWin() {
    // Wenn es ungespeicherte Würfe im aktuellen Set gibt, speichere diese
    if (currentSet.throws.length > 0) {
        const playerKey = `player${currentPlayer}`;
        const throwSet = {
            throws: [...currentSet.throws],
            total: currentSet.throws.reduce((a, b) => a + b, 0),
            imuData: {
                angles: [...currentSet.imuData.angles],
                velocities: [...currentSet.imuData.velocities]
            },
            timestamp: new Date().toISOString()
        };
        
        // Füge das unvollständige Set zur Spielerhistorie hinzu
        currentGameThrows[playerKey].push(throwSet);
    }
    
    if (currentPlayer === 1) {
        p1Legs++;
        document.getElementById('legsPlayerOne').textContent = p1Legs;
    } else {
        p2Legs++;
        document.getElementById('legsPlayerTwo').textContent = p2Legs;
    }
    alert(`Spieler ${currentPlayer} hat das Leg gewonnen!`);
    
    // Reset für das neue Leg
    p1Score = STARTING_SCORE;
    p2Score = STARTING_SCORE;
    document.getElementById('count1').textContent = p1Score;
    document.getElementById('count2').textContent = p2Score;
    
    // Wechsel zum anderen Spieler für das nächste Leg
    currentPlayer = currentPlayer === 1 ? 2 : 1;
    document.getElementById('p1').classList.toggle('active');
    document.getElementById('p2').classList.toggle('active');
    
    // Reset des aktuellen Wurfsatzes und Dartzähler
    currentDarts = 0;
    currentSet = {
        throws: [],
        imuData: {
            angles: [],
            velocities: []
        }
    };
    
    // Aktualisiere die Statistiken nach dem Speichern des letzten Sets
    updateStats();
}
// ===============================
// DATEN-MANAGEMENT
// ===============================

// Speichert neue IMU-Daten
function addIMUData(angle, velocity) {
    // Nur speichern wenn noch Platz für Würfe ist
    if (currentSet.imuData.angles.length < 3) {
        currentSet.imuData.angles.push(angle);
        currentSet.imuData.velocities.push(velocity);
        console.log("IMU Daten hinzugefügt:", { angle, velocity });
        console.log("Aktuelle IMU Daten:", currentSet.imuData);
    }
}

// Erweiterte Statistik-Berechnung
function calculatePlayerStats(playerNumber) {
    const sets = currentGameThrows[`player${playerNumber}`];
    
    if (sets.length === 0) return {
        average: 0,
        highest: 0,
        numberOfSets: 0,
        minAngle: 0,
        maxAngle: 0,
        avgAngle: 0,
        minVelocity: 0,
        maxVelocity: 0,
        avgVelocity: 0
    };

    // Berechne Wurf-Statistiken
    const totalPoints = sets.reduce((sum, set) => sum + set.total, 0);
    const highest = Math.max(...sets.map(set => set.total));
    
    // Sammle alle IMU-Daten
    const allAngles = sets.flatMap(set => set.imuData.angles).filter(angle => angle != null);
    const allVelocities = sets.flatMap(set => set.imuData.velocities).filter(velocity => velocity != null);
    
    // Berechne IMU-Statistiken
    const minAngle = allAngles.length > 0 ? Math.min(...allAngles) : 0;
    const maxAngle = allAngles.length > 0 ? Math.max(...allAngles) : 0;
    const avgAngle = allAngles.length > 0 ? allAngles.reduce((a, b) => a + b, 0) / allAngles.length : 0;
    
    const minVelocity = allVelocities.length > 0 ? Math.min(...allVelocities) : 0;
    const maxVelocity = allVelocities.length > 0 ? Math.max(...allVelocities) : 0;
    const avgVelocity = allVelocities.length > 0 ? allVelocities.reduce((a, b) => a + b, 0) / allVelocities.length : 0;
    
    return {
        average: totalPoints / sets.length,
        highest: highest,
        numberOfSets: sets.length,
        minAngle,
        maxAngle,
        avgAngle,
        minVelocity,
        maxVelocity,
        avgVelocity
    };
}

// Aktualisiert alle Statistiken in der UI
function updateStats() {
    const p1Stats = calculatePlayerStats(1);
    const p2Stats = calculatePlayerStats(2);
    
    // Update Standard-Statistiken
    document.getElementById('p1avg').textContent = p1Stats.average.toFixed(1);
    document.getElementById('p2avg').textContent = p2Stats.average.toFixed(1);
    document.getElementById('p1high').textContent = p1Stats.highest;
    document.getElementById('p2high').textContent = p2Stats.highest;
    document.getElementById('p1games').textContent = p1Stats.numberOfSets;
    document.getElementById('p2games').textContent = p2Stats.numberOfSets;
    
    // Update IMU-Statistiken
    document.getElementById('p1angle').textContent = p1Stats.avgAngle.toFixed(1);
    document.getElementById('p2angle').textContent = p2Stats.avgAngle.toFixed(1);
    document.getElementById('p1velocity').textContent = p1Stats.avgVelocity.toFixed(2);
    document.getElementById('p2velocity').textContent = p2Stats.avgVelocity.toFixed(2);
    
    // Update Min/Max Anzeigen
    document.getElementById('p1angle-range').textContent = 
        `${p1Stats.minAngle.toFixed(1)}° - ${p1Stats.maxAngle.toFixed(1)}°`;
    document.getElementById('p2angle-range').textContent = 
        `${p2Stats.minAngle.toFixed(1)}° - ${p2Stats.maxAngle.toFixed(1)}°`;
    document.getElementById('p1velocity-range').textContent = 
        `${p1Stats.minVelocity.toFixed(2)} - ${p1Stats.maxVelocity.toFixed(2)}`;
    document.getElementById('p2velocity-range').textContent = 
        `${p2Stats.minVelocity.toFixed(2)} - ${p2Stats.maxVelocity.toFixed(2)}`;
    
    // Aktualisiere Wurf-Historie
    updateThrowHistory(1);
    updateThrowHistory(2);
}

// Aktualisiert die Wurf-Historie in der UI
function updateThrowHistory(playerNumber) {
    const historyContainer = document.getElementById(`p${playerNumber}ThrowHistory`);
    const throws = currentGameThrows[`player${playerNumber}`];
    
    // Leere den Container
    historyContainer.innerHTML = '';
    
    // Füge die letzten 10 Würfe hinzu (neueste zuerst)
    throws.slice().reverse().slice(0, 10).forEach((set, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        // Formatiere das Datum
        const date = new Date(set.timestamp);
        const timeStr = date.toLocaleTimeString();
        
        // Erstelle den HTML-Inhalt mit allen verfügbaren Daten
        const angleStr = set.imuData.angles.map(a => a !== null ? a.toFixed(1) + '°' : '--').join(', ');
        const velocityStr = set.imuData.velocities.map(v => v !== null ? v.toFixed(2) + ' m/s' : '--').join(', ');
        
        historyItem.innerHTML = `
            <span class="throw-number">#${throws.length - index}</span>
            <div class="throw-details">
                <div>Punkte: ${set.throws.join(' + ')} = ${set.total}</div>
                <div>Winkel: ${angleStr}</div>
                <div>Geschw.: ${velocityStr}</div>
            </div>
            <span class="throw-time">${timeStr}</span>
        `;
        
        historyContainer.appendChild(historyItem);
    });
}

// Fügt einen neuen Punktwurf hinzu
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
        
        // Füge das Set zur Spielerhistorie hinzu
        currentGameThrows[playerKey].push(throwSet);
        
        // Reset currentSet
        currentSet = {
            throws: [],
            imuData: {
                angles: [],
                velocities: []
            }
        };
        
        console.log(`Neues Set für Spieler ${playerNumber} gespeichert:`, throwSet);
    }
    
    // Aktualisiere die Statistiken
    updateStats();
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

// Event-Handler für neue IMU-Daten vom Server
// Event-Handler für neue IMU-Daten vom Server
async function handleNewIMUData(data) {
    if (data.last_relative_roll !== null) {
        // Aktualisiere die Anzeige der aktuellen Werte
        document.getElementById('current-angle').textContent = 
            data.last_relative_roll.toFixed(1);
            
        // Berechne Gesamtgeschwindigkeit
        const velocity = data.velocity.total || 0;
        document.getElementById('current-velocity').textContent = 
            velocity.toFixed(2);
    }
}

// Fügt neue IMU-Daten zum aktuellen Set hinzu
function addIMUData(angle, velocity) {
    // Speichere nur wenn der Wurf registriert wurde und Platz ist
    if (currentSet.imuData.angles.length < 3 && angle !== null && velocity !== null) {
        currentSet.imuData.angles.push(angle);
        currentSet.imuData.velocities.push(velocity);
        console.log("Neue IMU Daten hinzugefügt:", { angle, velocity });
        console.log("Aktuelle IMU Daten:", currentSet.imuData);
    }
}

// Überschreibe die fetchData Funktion
async function fetchData() {
    try {
        const response = await fetch('/data');
        const data = await response.json();
        handleNewIMUData(data);
    } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
    }
}

// Fügt einen neuen Punktwurf hinzu
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
        
        // Füge das Set zur Spielerhistorie hinzu
        currentGameThrows[playerKey].push(throwSet);
        
        console.log(`Neues Set für Spieler ${playerNumber} gespeichert:`, throwSet);
        
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

// Daten-Abruf starten
setInterval(fetchData, 100);

// ===============================
// SPIEL INITIALISIERUNG
// ===============================

createNumberButtons();