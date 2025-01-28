// ===============================
// KONSTANTEN & GLOBALE VARIABLEN
// ===============================

// Spielstand und Spieler-Status
let currentPlayer = 1;          // Aktiver Spieler (1 oder 2)
let p1Score = 501;             // Punktestand Spieler 1
let p2Score = 501;             // Punktestand Spieler 2
let currentDarts = 0;          // Anzahl der geworfenen Darts in der aktuellen Runde
let currentMultiplier = 1;     // Aktiver Multiplikator (1 = Single, 2 = Double, 3 = Triple)
let p1Legs = 0;               // Anzahl der gewonnenen Legs von Spieler 1
let p2Legs = 0;              // Anzahl der gewonnenen Legs von Spieler 2

// Spiel-Konfiguration
const maxDartsPerTurn = 3;     // Maximale Anzahl Darts pro Spieler pro Runde
const STARTING_SCORE = 501;    // Startpunktzahl für jeden Spieler

// Tracking der Würfe für Statistiken
let currentGameThrows = {
    player1: [],               // Array für alle Würfe von Spieler 1
    player2: []               // Array für alle Würfe von Spieler 2
};

// ===============================
// SPIELFELD-GENERIERUNG
// ===============================

/**
 * Erstellt alle Zahlen-Buttons und Multiplikator-Buttons im Spielfeld
 * Wird beim Start des Spiels aufgerufen
 */
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
    
    // Erstelle Bull's Eye Button (25)
    createBullButton(singles);
    
    // Erstelle Multiplikator-Buttons (Double/Triple)
    createModifierButtons(modifiers);
}

/**
 * Erstellt den Bull's Eye Button (25)
 * @param {HTMLElement} container - Container für den Button
 */
function createBullButton(container) {
    const bull25 = document.createElement('button');
    bull25.textContent = '25';
    bull25.id = 'single25';
    bull25.className = 'number-button';
    bull25.onclick = () => updateScore(25 * currentMultiplier);
    container.appendChild(bull25);
}

/**
 * Erstellt die Double und Triple Buttons
 * @param {HTMLElement} container - Container für die Buttons
 */
function createModifierButtons(container) {
    // Double Button
    const doubleBtn = document.createElement('button');
    doubleBtn.textContent = 'Double';
    doubleBtn.id = 'double';
    doubleBtn.className = 'modifier-button';
    doubleBtn.onclick = () => toggleModifier(2, doubleBtn);
    container.appendChild(doubleBtn);

    // Triple Button
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

/**
 * Verwaltet die Multiplikator-Buttons (Double/Triple)
 * @param {number} multiplier - Der zu setzende Multiplikator (2 oder 3)
 * @param {HTMLElement} button - Der geklickte Button
 */
function toggleModifier(multiplier, button) {
    if (currentMultiplier === multiplier) {
        // Deaktiviere den Multiplikator, wenn er bereits aktiv ist
        currentMultiplier = 1;
        button.classList.remove('active');
    } else {
        // Aktiviere den neuen Multiplikator
        const modifierButtons = document.querySelectorAll('.modifier-button');
        modifierButtons.forEach(btn => btn.classList.remove('active'));
        currentMultiplier = multiplier;
        button.classList.add('active');
    }
}

/**
 * Wechselt zwischen den Spielern und aktualisiert die UI
 */
function switchPlayer() {
    currentPlayer = currentPlayer === 1 ? 2 : 1;
    document.getElementById('p1').classList.toggle('active');
    document.getElementById('p2').classList.toggle('active');
}

/**
 * Aktualisiert den Punktestand nach einem Wurf
 * @param {number} points - Geworfene Punkte (bereits multipliziert)
 */
function updateScore(points) {
  if (points === 75) {
      console.error("Triple cannot be applied to 25.");
      alert("Triple cannot be applied to 25.");
      return;
  }

  const scoreElement = currentPlayer === 1 ? document.getElementById('count1') : document.getElementById('count2');
  const currentScore = currentPlayer === 1 ? p1Score : p2Score;
  
  if (currentScore - points >= 0) {
      addThrowToCurrentGame(currentPlayer, points);
      
      scoreElement.classList.add('updating');
      
      if (currentPlayer === 1) {
          p1Score -= points;
          scoreElement.textContent = p1Score;
      } else {
          p2Score -= points;
          scoreElement.textContent = p2Score;
      }

      setTimeout(() => {
          scoreElement.classList.remove('updating');
      }, 300);

      if (currentScore - points === 0) {
          // Erhöhe den Leg-Counter für den Gewinner
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

      const modifierButtons = document.querySelectorAll('.modifier-button');
      modifierButtons.forEach(btn => btn.classList.remove('active'));
      
      currentMultiplier = 1;
      currentDarts++;
      
      if (currentDarts >= maxDartsPerTurn) {
          switchPlayer();
          currentDarts = 0;
      }
  }
}

/**
 * Aktualisiert die Punkteanzeige mit Animation
 * @param {HTMLElement} scoreElement - Das Score-Element in der UI
 * @param {number} points - Abzuziehende Punkte
 */
function updateScoreDisplay(scoreElement, points) {
    scoreElement.classList.add('updating');
    
    if (currentPlayer === 1) {
        p1Score -= points;
        scoreElement.textContent = p1Score;
    } else {
        p2Score -= points;
        scoreElement.textContent = p2Score;
    }

    setTimeout(() => {
        scoreElement.classList.remove('updating');
    }, 300);
}

/**
 * Bereitet den nächsten Wurf vor oder wechselt den Spieler
 */
function prepareNextThrow() {
    // Reset Multiplikator
    const modifierButtons = document.querySelectorAll('.modifier-button');
    modifierButtons.forEach(btn => btn.classList.remove('active'));
    currentMultiplier = 1;
    
    // Erhöhe Wurf-Zähler
    currentDarts++;
    
    // Wechsle Spieler nach 3 Würfen
    if (currentDarts >= maxDartsPerTurn) {
        switchPlayer();
        currentDarts = 0;
    }
}

// ===============================
// STATISTIK-FUNKTIONEN
// ===============================

/**
 * Fügt einen Wurf zur Statistik hinzu
 * @param {number} playerNumber - Spielernummer (1 oder 2)
 * @param {number} points - Geworfene Punkte
 */
function addThrowToCurrentGame(playerNumber, points) {
    const playerKey = `player${playerNumber}`;
    currentGameThrows[playerKey].push(points);
}

/**
 * Berechnet den 3-Dart-Average für einen Spieler
 * @param {Array} throws - Array mit allen Würfen des Spielers
 * @returns {number} - Durchschnitt über alle 3-Dart-Serien
 */
function calculateThreeDartAverage(throws) {
    if (throws.length === 0) return 0;
    
    let sumOfSets = 0;
    let completeSets = Math.floor(throws.length / 3);
    
    // Berechne nur vollständige 3-Dart-Serien
    for (let i = 0; i < completeSets; i++) {
        sumOfSets += throws[i * 3] + throws[i * 3 + 1] + throws[i * 3 + 2];
    }
    
    return completeSets === 0 ? 0 : (sumOfSets / completeSets);
}

/**
 * Findet die höchste 3-Dart-Kombination eines Spielers
 * @param {Array} throws - Array mit allen Würfen des Spielers
 * @returns {number} - Höchste Punktzahl in einer 3-Dart-Serie
 */
function findHighestThreeDarts(throws) {
    if (throws.length < 3) return 0;
    
    let highest = 0;
    for (let i = 0; i <= throws.length - 3; i += 3) {
        const sum = throws[i] + throws[i + 1] + throws[i + 2];
        if (sum > highest) highest = sum;
    }
    return highest;
}

// ===============================
// SPIEL-MANAGEMENT
// ===============================

function resetLeg() {
  p1Score = 501;
  p2Score = 501;
  currentDarts = 0;
  document.getElementById('count1').textContent = p1Score;
  document.getElementById('count2').textContent = p2Score;
  resetGameStats();
}
/**
 * Setzt das Spiel auf den Ausgangszustand zurück
 */
function resetGame() {
  p1Score = 501;
  p2Score = 501;
  currentPlayer = 1;
  currentDarts = 0;
  // Setze auch die Legs zurück
  p1Legs = 0;
  p2Legs = 0;
  document.getElementById('count1').textContent = p1Score;
  document.getElementById('count2').textContent = p2Score;
  document.getElementById('legsPlayerOne').textContent = '0';
  document.getElementById('legsPlayerTwo').textContent = '0';
  document.getElementById('p1').classList.add('active');
  document.getElementById('p2').classList.remove('active');
  resetGameStats();
}

/**
 * Setzt die Statistiken zurück
 */
function resetGameStats() {
    currentGameThrows = {
        player1: [],
        player2: []
    };
}

// ===============================
// STATISTIK-MODAL
// ===============================

// Modal-Element-Referenzen
const modal = document.getElementById('statsModal');
const statsBtn = document.getElementById('showStats');
const span = document.getElementsByClassName('close')[0];

// Modal Event-Listener
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

/**
 * Aktualisiert die Statistik-Anzeige im Modal
 */
function updateStats() {
    // Statistiken für Spieler 1
    updatePlayerStats(1);
    // Statistiken für Spieler 2
    updatePlayerStats(2);
}

/**
 * Aktualisiert die Statistiken für einen Spieler
 * @param {number} playerNumber - Spielernummer (1 oder 2)
 */
function updatePlayerStats(playerNumber) {
    const throws = currentGameThrows[`player${playerNumber}`];
    const stats = {
        threeDartAverage: calculateThreeDartAverage(throws),
        highestThreeDarts: findHighestThreeDarts(throws),
        numberOfThrows: throws.length
    };
    
    document.getElementById(`p${playerNumber}avg`).textContent = stats.threeDartAverage.toFixed(1);
    document.getElementById(`p${playerNumber}high`).textContent = stats.highestThreeDarts;
    document.getElementById(`p${playerNumber}games`).textContent = Math.floor(stats.numberOfThrows / 3);
}

// ===============================
// EVENT LISTENER
// ===============================

// Setup-Formular
document.getElementById('setupForm').addEventListener('submit', (e) => {
    e.preventDefault();
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';
    
    // Spielernamen setzen
    const p1Name = document.getElementById('player1').value;
    const p2Name = document.getElementById('player2').value;
    document.getElementById('playerOneName').textContent = p1Name;
    document.getElementById('playerTwoName').textContent = p2Name;
});

// Spielsteuerung
document.getElementById('nextPlayerButton').addEventListener('click', () => {
    switchPlayer();
    currentDarts = 0;
});

document.getElementById('nextgame').addEventListener('click', resetGame);

// ===============================
// SPIEL INITIALISIERUNG
// ===============================

// Starte das Spiel
createNumberButtons();