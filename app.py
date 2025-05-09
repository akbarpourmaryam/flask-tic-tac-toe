from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    room = request.args.get("room")
    name = request.args.get("name", "Anonymous")
    size = int(request.args.get("size", 3))
    return render_template("game.html", room=room, name=name, size=size)

@socketio.on("join")
def on_join(data):
    room = data["room"]
    name = data.get("name", "Anonymous")
    join_room(room)
    emit("player_joined", {"room": room, "name": name}, room=room)

@socketio.on("move")
def on_move(data):
    room = data["room"]
    emit("move_made", data, room=room)

@socketio.on("restart")
def on_restart(data):
    room = data["room"]
    emit("game_reset", {}, room=room)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
