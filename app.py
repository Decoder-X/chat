from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import random
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# List of bad words to filter
BAD_WORDS = ['badword1', 'badword2', 'examplebadword']  # Add your words here

# Function to filter bad words
def filter_bad_words(message):
    # Replace each bad word with asterisks
    for word in BAD_WORDS:
        message = re.sub(r'\b' + re.escape(word) + r'\b', '*' * len(word), message, flags=re.IGNORECASE)
    return message

nicknames = {}

@app.route('/')
def index():
    return render_template('index.html')

chat_history = []


@socketio.on('message')
def handle_message(msg):
    clean_msg = filter_bad_words(msg)
    sender_id = request.sid
    nickname = nicknames.get(sender_id, "Unknown")
    full_msg = {
        'text': f"{nickname}: {clean_msg}",
        'sender': sender_id
    }
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
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0', port=10000)
