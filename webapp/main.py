#!/usr/bin/env python3

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from threading import Thread
import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

thread = None

class data:
    target_position = 0;
    current_position = 0;

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        time.sleep(0.1)
        data.current_position += 1;
        socketio.emit('update parameters',
            {'currentPosition': data.current_position,
            'targetPosition': data.target_position,
            'uptime': str(datetime.datetime.now())
            },
            namespace='/test')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')

@socketio.on('set target position', namespace='/test')
def test_message(message):
    global data
    data.target_position = message['targetPositionValue']
    emit('update parameters',
         {'currentPosition': data.current_position, 'targetPosition': data.target_position})

if __name__ == '__main__':
    socketio.run(app, debug=True)

