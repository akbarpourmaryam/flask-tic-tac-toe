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
    join_room(data["room"])
    emit("player_joined", {"room": data["room"], "name": data.get("name", "Anonymous")}, room=data["room"])

@socketio.on("move")
def on_move(data):
    emit("move_made", data, room=data["room"])

@socketio.on("restart")
def on_restart(data):
    emit("game_reset", {}, room=data["room"])

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
