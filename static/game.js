const socket = io();
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const restartBtn = document.getElementById("restartBtn");

let board = Array(size).fill().map(() => Array(size).fill(0));
let isMyTurn = false;
let playerId = null;
let winner = null;

// Set CSS grid
boardEl.style.setProperty("grid-template-columns", `repeat(${size}, 1fr)`);

// Emit join on page load
socket.emit("join", { room, name: playerName });

// ✅ When a player joins — log only
socket.on("player_joined", (data) => {
  console.log(`${data.name} joined the room.`);
});

// ✅ Start game once two players are in the room
socket.on("start_game", (data) => {
    const playerInfo = data.players.find(p => p.name === playerName);
    if (!playerInfo) {
      console.error("Could not find this player in start_game data");
      return;
    }
  
    playerId = playerInfo.player;
    isMyTurn = (playerId === 1);
    statusEl.innerText = isMyTurn ? "Your turn" : "Waiting for opponent...";
    renderBoard();
  });
  

// Optional: if a 3rd person tries to join
socket.on("room_full", () => {
  alert("Room is full. Only 2 players can join.");
});

// When a move is made
socket.on("move_made", (data) => {
  const { row, col, player } = data;
  board[row][col] = player;
  isMyTurn = (playerId !== player);
  renderBoard();

  const result = checkWinner(board);
  if (result) {
    winner = result.player;
    if (result.draw) {
      statusEl.innerText = "It's a draw!";
    } else {
      statusEl.innerText = `Player ${winner} wins!`;
      highlightWinningCells(result.line);
    }
    restartBtn.style.display = "inline";
  } else {
    statusEl.innerText = isMyTurn ? "Your turn" : "Waiting for opponent...";
  }
});

socket.on("game_reset", () => {
  board = Array(size).fill().map(() => Array(size).fill(0));
  winner = null;
  isMyTurn = (playerId === 1);
  statusEl.innerText = isMyTurn ? "Your turn" : "Waiting for opponent...";
  restartBtn.style.display = "none";
  renderBoard();
});

restartBtn.addEventListener("click", () => {
  socket.emit("restart", { room });
});

function renderBoard() {
    console.log("⚙️ renderBoard called");
    console.log("Current board state:", board);
    console.log("Player ID:", playerId, "Is my turn?", isMyTurn, "Winner:", winner);
  
    boardEl.innerHTML = '';
    board.forEach((row, r) => {
      row.forEach((cell, c) => {
        const div = document.createElement("div");
        div.classList.add("cell");
  
        if (cell === 1) {
          div.textContent = "X";
          div.classList.add("taken", "player-1");
        } else if (cell === 2) {
          div.textContent = "O";
          div.classList.add("taken", "player-2");
        }
  
        if (cell === 0 && isMyTurn && !winner) {
          div.addEventListener("click", () => {
            console.log(`🖱️ Clicked on cell [${r}, ${c}]`);
            socket.emit("move", { room, row: r, col: c, player: playerId });
          });
        } else {
          div.classList.add("taken");
        }
  
        boardEl.appendChild(div);
      });
    });
  }
  

function checkWinner(board) {
  for (let i = 0; i < size; i++) {
    if (board[i][0] && board[i].every(cell => cell === board[i][0]))
      return { player: board[i][0], line: board[i].map((_, idx) => [i, idx]) };

    const col = board.map(row => row[i]);
    if (col[0] && col.every(cell => cell === col[0]))
      return { player: col[0], line: col.map((_, idx) => [idx, i]) };
  }

  const main = board.map((row, i) => row[i]);
  if (main[0] && main.every(cell => cell === main[0]))
    return { player: main[0], line: main.map((_, i) => [i, i]) };

  const anti = board.map((row, i) => row[size - i - 1]);
  if (anti[0] && anti.every(cell => cell === anti[0]))
    return { player: anti[0], line: anti.map((_, i) => [i, size - i - 1]) };

  if (board.flat().every(cell => cell !== 0)) {
    return { player: null, draw: true };
  }

  return null;
}

function highlightWinningCells(cells) {
  const cellDivs = boardEl.querySelectorAll(".cell");
  cells.forEach(([r, c]) => {
    const idx = r * size + c;
    cellDivs[idx].classList.add("winner");
  });
}
