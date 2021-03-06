#Brandon Nguyen and Rojan Rijal
#April 28, 2020
from datetime import datetime
import os, requests
from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError
from flask_cors import CORS
from db import create_conversation,get_messages, send_message

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
socketio = SocketIO(app,cors_allowed_origins="https://internmate.tech")

CORS(app)

def allowed():
    allowed_or_not = requests.get('https://internmate.tech/api/user_exists/{id}'.format(id=session['profile']['user_id'])).json()
    return allowed_or_not['status']

#Loads messages that was sent by the users
@socketio.on('load_message')
def load_messages(data):
    if allowed():
        messages = get_messages(data['conversation_id'])
        socketio.emit('show_messages', dumps(messages))

#Function adds a timestamp to messafes and the sets the conv. id, profile, user id, and message
#Socketio.emit display that the message was received 
@socketio.on('send_message')
def handle_send_message_event(data):
    if allowed():
        data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
        send_message(data['conv_id'],
                    session['profile']['user_id'],
                    data['message'])
        socketio.emit('receive_message', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
