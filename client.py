import socketio

sio = socketio.Client()


@sio.on('connect')
def connect():
    connected = True
    print('connection established')
    print('insira o texto a ser enviado ao servidor:')
    while connected:
        data = input()
        if data == '/exit':
            connected = False
            sio.disconnect()
        else:
            sio.emit('test', data)


@sio.on('connected')
def connected(data):
    print('server sid: ', data)


@sio.on('disconnect')
def disconnect():
    print('disconnecting from the server...')


@sio.on('new_connection')
def onNewConnection(sid):
    print(f'new connection from: {sid}')


sio.connect('http://localhost:5000')
sio.wait()
