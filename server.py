import os
from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sockets = SocketIO(app, ping_interval=1)

connections = []
ready = 0


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
    global ready
    ready = 0
    sid = request.sid
    ip = request.remote_addr

    bigPrint(f'connected: {ip} - {sid}')

    sockets.emit('connected', sid)
    data = {'add': connections}
    sockets.emit('connections', data, broadcast=True)

    data = {
        'player': len(connections)+1,
        'sid': sid
    }
    sockets.emit('player', data, to=sid)
    sockets.emit('2-player-join', data, skip_sid=sid)
    for player in connections:
        if player:
            data = {
                'player': connections.index(player)+1,
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


@sockets.on('tap')
def onTap():
    sid = request.sid
    sockets.emit('tap', skip_sid=sid)


@sockets.on('get-client-data')
def onGetClientData(data):
    sid = request.sid
    sockets.emit('get-server-data', data, skip_sid=sid)


@sockets.on('get-client-ready')
def onGetClientReady(data):
    global ready
    sid = request.sid
    sockets.emit('get-server-ready', skip_sid=sid)
    ready += 1

    if ready == 2:
        sockets.emit('server-start-game')


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
