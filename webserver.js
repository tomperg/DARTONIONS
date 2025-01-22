let currentPlayer = 1;
let p1Score = 501;
let p2Score = 501;
let currentDarts = 0; // Anzahl der Darts des aktuellen Spielers
const maxDartsPerTurn = 3; // Maximale Darts pro Spieler pro Runde
const totalPlayers = 2; // Anzahl der Spieler (z. B. 2 Spieler)

function createNumberButtons() {
  const singles = document.getElementById('singles');
  const modifiers = document.getElementById('modifiers');

  // Singles
  for(let i = 1; i <= 20; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;
    btn.id = `single${i}`;
    btn.className = 'number-button';
    btn.onclick = () => updateScore(i * currentMultiplier);
    singles.appendChild(btn);
  }
  
  // Bull
  const bull25 = document.createElement('button');
  bull25.textContent = '25';
  bull25.id = 'single25';
  bull25.className = 'number-button';
  bull25.onclick = () => updateScore(25 * currentMultiplier);
  singles.appendChild(bull25);

  // Modifiers
  const doubleBtn = document.createElement('button');
  doubleBtn.textContent = 'Double';
  doubleBtn.id = 'double';
  doubleBtn.className = 'modifier-button';
  doubleBtn.onclick = () => toggleModifier(2,doubleBtn);
  modifiers.appendChild(doubleBtn);

  const tripleBtn = document.createElement('button');
  tripleBtn.textContent = 'Triple';
  tripleBtn.id = 'triple';
  tripleBtn.className = 'modifier-button';
  tripleBtn.onclick = () => toggleModifier(3,tripleBtn);
  modifiers.appendChild(tripleBtn);
}

let currentMultiplier = 1;

function setMultiplier(multiplier) {
  currentMultiplier = multiplier;

  // Entferne die aktive Klasse von allen Modifier-Buttons
  const modifierButtons = document.querySelectorAll('.modifier-button');
  modifierButtons.forEach(btn => btn.classList.remove('active'));

  // Füge die aktive Klasse zum geklickten Button hinzu
  const activeButton = multiplier === 2 ? document.getElementById('double') : document.getElementById('triple');
  activeButton.classList.add('active');

  console.log(`Current multiplier set to: ${multiplier}`);
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

  const scoreElement = currentPlayer === 1 ? document.getElementById('count1') : document.getElementById('count2');
  const currentScore = currentPlayer === 1 ? p1Score : p2Score;
  
  if (currentScore - points >= 0) {
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
      alert(`Spieler ${currentPlayer} hat gewonnen!`);
      resetGame();
    }
    const modifierButtons = document.querySelectorAll('.modifier-button');
    modifierButtons.forEach(btn => btn.classList.remove('active'));
    
    // Setze den Multiplikator zurück auf 1
    currentMultiplier = 1;
    currentDarts++;
    // Prüfe, ob der Spieler drei Darts geworfen hat
    if (currentDarts >= maxDartsPerTurn) {
      // Wechsle den Spieler
      switchPlayer();
      currentDarts = 0; // Reset der Dart-Anzahl für den neuen Spieler
    }
  }
}


function toggleModifier(multiplier, button) {
  if (currentMultiplier === multiplier) {
    // Falls der aktuelle Modifier aktiv ist, zurücksetzen
    currentMultiplier = 1;
    button.classList.remove('active');
  } else {
    // Falls ein anderer Modifier aktiv ist, aktualisieren
    const modifierButtons = document.querySelectorAll('.modifier-button');
    modifierButtons.forEach(btn => btn.classList.remove('active'));

    currentMultiplier = multiplier;
    button.classList.add('active');
  }
  }



function resetGame() {
  p1Score = 501;
  p2Score = 501;
  currentPlayer = 1;
  document.getElementById('count1').textContent = p1Score;
  document.getElementById('count2').textContent = p2Score;
  document.getElementById('p1').classList.add('active');
  document.getElementById('p2').classList.remove('active');
}

// Event Listeners
document.getElementById('setupForm').addEventListener('submit', (e) => {
  e.preventDefault();
  document.getElementById('startScreen').style.display = 'none';
  document.getElementById('gameScreen').style.display = 'block';
  
  const p1Name = document.getElementById('player1').value;
  const p2Name = document.getElementById('player2').value;
  document.getElementById('playerOneName').textContent = p1Name;
  document.getElementById('playerTwoName').textContent = p2Name;
});

document.getElementById('nextPlayerButton').addEventListener('click', switchPlayer);
document.getElementById('nextgame').addEventListener('click', resetGame);

// Initialisierung
createNumberButtons();