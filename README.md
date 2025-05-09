# 🎮 Flask Tic Tac Toe (Multiplayer, N x N)

A real-time multiplayer Tic Tac Toe game built with Flask and Flask-SocketIO. Two users can join the same room from different devices, choose board size, and play live.

![screenshot](docs/screenshot.png) <!-- Add one later if you'd like -->

---

## 🚀 Features

- 🔁 Real-time two-player gameplay via WebSockets
- 🧠 Configurable board size (e.g., 3x3, 4x4, 5x5...)
- 🎨 Player names, colors, and winning highlights
- 🔄 Restart/rematch button after game ends
- 📱 Mobile-friendly layout
- ☁️ Deployed via [Render](https://render.com)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO
- **Frontend:** HTML, CSS, JavaScript
- **Real-Time:** Socket.IO
- **Deployment:** Render (free hosting)

---

## 🧑‍💻 Run Locally

### 1. Clone & set up environment

```bash
git clone https://github.com/yourusername/flask-tic-tac-toe.git
cd flask-tic-tac-toe
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🌐 Deploy to Render (Free)

### ✅ One-time setup

1. Push to a GitHub repo
2. Go to [https://render.com](https://render.com)
3. Click **"New Web Service"**
4. Connect your GitHub repo
5. Settings:

| Setting           | Value               |
|-------------------|---------------------|
| Runtime           | Python              |
| Build Command     | `pip install -r requirements.txt` |
| Start Command     | `python app.py`     |
| Environment       | Add `ASYNC_MODE = eventlet` |
| Port binding      | Automatically from `os.environ.get("PORT")` |

### ⚠️ Important

Make sure the **bottom of `app.py`** looks like this:

```python
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
```

---

## 📁 Project Structure

```
flask-tic-tac-toe/
├── app.py
├── Procfile
├── requirements.txt
├── templates/
│   ├── index.html
│   └── game.html
├── static/
│   ├── styles.css
│   └── game.js
```

---

## ✅ Next Improvements

- [ ] Confetti animation on win 🎉
- [ ] Add computer AI fallback (minimax)
- [ ] Save player stats or leaderboard
- [ ] Chat between players in-game
- [ ] Shareable room links

---

## 🙋‍♀️ Author

**Maryam Akbarpour**  
[GitHub](https://github.com/akbarpourmaryam)

---

### ⭐️ Like this project?

Star it on GitHub and share with a friend!
