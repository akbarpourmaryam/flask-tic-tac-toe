from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # needed for sessions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        n = int(request.form["size"])
        mode = request.form["mode"]  # "human" or "ai"
        session["n"] = n
        session["mode"] = mode
        session["board"] = [[0] * n for _ in range(n)]
        session["turn"] = 1  # Player 1 starts
        return redirect(url_for("game"))
    
    return render_template("index.html")


def get_ai_move(board):
    best_score = float('-inf')
    move = None
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                board[r][c] = 2  # AI plays
                score = minimax(board, False)
                board[r][c] = 0
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def minimax(board, is_maximizing):
    winner = check_winner(board, len(board))
    if winner == 2:
        return 1
    elif winner == 1:
        return -1
    elif all(cell != 0 for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 0:
                    board[r][c] = 2
                    score = minimax(board, False)
                    board[r][c] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 0:
                    board[r][c] = 1
                    score = minimax(board, True)
                    board[r][c] = 0
                    best_score = min(score, best_score)
        return best_score


@app.route("/game", methods=["GET", "POST"])
def game():
    n = session["n"]
    board = session["board"]
    turn = session["turn"]
    winner = check_winner(board, n)

    if request.method == "POST":
        row = int(request.form["row"])
        col = int(request.form["col"])
        if board[row][col] == 0 and winner == 0:
            board[row][col] = turn
            session["turn"] = 2 if turn == 1 else 1
            session["board"] = board
            winner = check_winner(board, n)

            # AI Move
            if session["mode"] == "ai" and session["turn"] == 2 and winner == 0:
                ai_row, ai_col = get_ai_move(board)
                board[ai_row][ai_col] = 2
                session["turn"] = 1
                session["board"] = board
                winner = check_winner(board, n)

    return render_template("game.html", board=board, n=n, turn=session["turn"], winner=winner)


def check_winner(board, n):
    for i in range(n):
        if all(cell == 1 for cell in board[i]) or all(cell == 2 for cell in board[i]):
            return board[i][0]
        if all(row[i] == 1 for row in board) or all(row[i] == 2 for row in board):
            return board[0][i]
    if all(board[i][i] == 1 for i in range(n)) or all(board[i][i] == 2 for i in range(n)):
        return board[0][0]
    if all(board[i][n-i-1] == 1 for i in range(n)) or all(board[i][n-i-1] == 2 for i in range(n)):
        return board[0][n-1]
    if all(cell != 0 for row in board for cell in row):
        return "0"  # draw

    return 0

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
