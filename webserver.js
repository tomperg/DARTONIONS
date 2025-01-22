let currentPlayer = 1;
let p1Score = 501;
let p2Score = 501;

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
  
  // Bull's Eye
  const bull25 = document.createElement('button');
  bull25.textContent = '25';
  bull25.id = 'single25';
  bull25.className = 'number-button';
  bull25.onclick = () => updateScore(25 * currentMultiplier);
  singles.appendChild(bull25);
  
  const bull50 = document.createElement('button');
  bull50.textContent = '50';
  bull50.id = 'single50';
  bull50.className = 'number-button';
  bull50.onclick = () => updateScore(50 * currentMultiplier);
  singles.appendChild(bull50);

  // Modifiers
  const doubleBtn = document.createElement('button');
  doubleBtn.textContent = 'Double';
  doubleBtn.id = 'double';
  doubleBtn.className = 'modifier-button';
  doubleBtn.onclick = () => setMultiplier(2);
  modifiers.appendChild(doubleBtn);

  const tripleBtn = document.createElement('button');
  tripleBtn.textContent = 'Triple';
  tripleBtn.id = 'triple';
  tripleBtn.className = 'modifier-button';
  tripleBtn.onclick = () => setMultiplier(3);
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


function updateScore(points) {
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
  }
}

function switchPlayer() {
  currentPlayer = currentPlayer === 1 ? 2 : 1;
  document.getElementById('p1').classList.toggle('active');
  document.getElementById('p2').classList.toggle('active');
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