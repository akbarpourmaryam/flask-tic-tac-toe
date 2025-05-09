# ✅ MONKEY PATCH FIRST
import eventlet
eventlet.monkey_patch()

# ✅ THEN import everything else
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
room_players = {}

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    room = request.args.get("room")
    name = request.args.get("name", "Anonymous")
    size = int(request.args.get("size", 3))
    return render_template("game.html", room=room, name=name, size=size)

# SocketIO events
@socketio.on("join")
def on_join(data):
    room = data["room"]
    name = data.get("name", "Anonymous")
    join_room(room)
    emit("player_joined", {"room": room, "name": name}, room=room)

@socketio.on("move")
def on_move(data):
    emit("move_made", data, room=data["room"])

@socketio.on("restart")
def on_restart(data):
    emit("game_reset", {}, room=data["room"])

@socketio.on("join")
def on_join(data):
    room = data["room"]
    name = data.get("name", "Anonymous")

    # initialize if not seen
    if room not in room_players:
        room_players[room] = []

    # limit to 2 players
    if len(room_players[room]) >= 2:
        emit("room_full", {}, room=request.sid)
        return

    player_number = len(room_players[room]) + 1
    room_players[room].append(player_number)

    join_room(room)

    emit("player_joined", {
        "room": room,
        "name": name,
        "player": player_number
    }, room=request.sid)


# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
