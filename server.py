import os
from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sockets = SocketIO(app, ping_interval=1)

connections = []


def bigPrint(*args):
    print()
    print()
    for text in args:
        print(text)
    print()
    print()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# Start of socketio events configuration
# request.sid = client session id, used to identify the client


@sockets.on('connect')
def onConnect():
    global connections
    sid = request.sid
    ip = request.remote_addr


    bigPrint(f'connected: {ip} - {sid}')

    sockets.emit('connected', sid)
    data = {'add': connections}
    sockets.emit('connections', data, broadcast=True)
    
    data = {
        'first': True,
        'sid': sid
        }
    sockets.emit('2-player-join', data, skip_sid=sid)
    for player in connections:
        if player:
            data = {
                'second': True,
                'sid': player
            }
            sockets.emit('2-player-join', data, to=sid)
    
    connections.append(sid)

@sockets.on('score')
def onScore(score):
    sid = request.sid    
    bigPrint(f'player {sid} scored {score}')
    data = {sid: score}
    sockets.emit('score', data, broadcast=True)
    


@sockets.on('test')
def test(message):
    sid = request.sid
    bigPrint(message)

    sockets.emit('test', message, to=sid)


@sockets.on('disconnect')
def onDisconnect():
    global connections
    sid = request.sid
    ip = request.remote_addr

    connections.remove(sid)
    data = {'remove': connections}
    sockets.emit('connections', data, broadcast=True)
    
    data = {
        'sid': sid
        }
    sockets.emit('2-player-leave', data, skip_sid=sid)

    print(f'disconnected {sid}')

    # End of socketio events configuration


sockets.run(app, debug=True, host="0.0.0.0", port=5001)
