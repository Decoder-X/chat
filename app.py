from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

nicknames = {}

@app.route('/')
def index():
    return render_template('index.html')

chat_history = []

@socketio.on('message')
def handle_message(msg):
    nickname = nicknames.get(str(request.sid), "Unknown")
    full_msg = f"{nickname}: {msg}"
    chat_history.append(full_msg)
    send(full_msg, broadcast=True)

@socketio.on('connect')
def connect(auth):
    nickname = "User" + str(random.randint(1000, 9999))
    nicknames[str(request.sid)] = nickname
    for msg in chat_history:
        send(msg)

@socketio.on('disconnect')
def disconnect():
    nickname = nicknames.pop(str(request.sid), "Unknown")
    print(f"{nickname} disconnected.")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="5000", debug=True)