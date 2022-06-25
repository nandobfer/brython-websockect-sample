from browser import bind, document, websocket, window, html

sid = None
score = 0
connections = []


class Client():
    def __init__(self, sid, element):
        self.sid = sid
        self.element = element
        self.score = 0


def on_connected(data):
    global sid
    sid = data
    document['sid'].text = f"Client SID = {sid}"


def on_open():
    document['btn-disconnect'].disabled = False
    document['btn-send'].disabled = False
    document['btn-connect'].disabled = True
    document['status'].text = f"Connected to server."
    document['connections-container'] <= html.DIV(Id='connections')
    document['connections'] <= html.P('connections')


def on_message(evt):
    # message received from server
    document['status'].text = f"Message received : {evt}"


def on_close(evt):
    # websocket is closed
    document['status'].text = "Connection is closed"
    document['sid'].text = ""
    document['btn-connect'].disabled = False
    document['btn-disconnect'].disabled = True
    document['btn-send'].disabled = True
    document['connections'].remove()


def renderConnections(data):
    element = document['connections']

    if 'add' in data:
        for sid in data['add']:
            client = getClient(sid)
            if not client in connections:
                client = Client(sid, html.P(f'{sid} - SCORE: 0', Id=sid))
                element <= client.element
                connections.append(client)
    elif 'remove' in data:
        for client in connections:
            if not client.sid in data['remove']:
                document[client.sid].remove()
                connections.remove(client)
                
def onScore(data):
    for sid in data:
        client = getClient(sid)
        client.score = data[sid]
        document[sid].text = f'{sid} - SCORE: {client.score}'
        
def getClient(sid):
    for client in connections:
        if sid == client.sid:
            return client


sio = None


@ bind('#btn-connect', 'click')
def _open(ev):
    if not websocket.supported:
        document['status'].text = "WebSocket is not supported by your browser"
        return
    global sio
    # open a web socket
    # sio = websocket.WebSocket("sio://127.0.0.1:5000/")
    sio = window.io.connect('44.206.122.252:5001/')
    # bind functions to web socket events
    sio.on('connect', on_open)
    sio.on('connected', on_connected)
    sio.on('test', on_message)
    sio.on('disconnect', on_close)
    sio.on('connections', renderConnections)
    sio.on('score', onScore)


@ bind('#btn-send', 'click')
def send(ev):
    global score
    data = document["data"].value
    if data:
        if data == '/score':
            score += 1
            sio.emit('score', score)
        sio.emit('test', data)


@ bind('#btn-disconnect', 'click')
def close_connection(ev):
    sio.close()
    document['btn-connect'].disabled = False
