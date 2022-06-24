from browser import bind, document, websocket, window, html

sid = None
connections = []


class Client():
    def __init__(self, sid, element):
        self.sid = sid
        self.element = element


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
            if not sid in connections:
                client = Client(sid, html.P(f'{sid}', Id=sid))
                element <= client.element
                connections.append(sid)
    elif 'remove' in data:
        for sid in connections:
            if not sid in data['remove']:
                document[sid].remove()
                connections.remove(sid)


sio = None


@ bind('#btn-connect', 'click')
def _open(ev):
    if not websocket.supported:
        document['status'].text = "WebSocket is not supported by your browser"
        return
    global sio
    # open a web socket
    # sio = websocket.WebSocket("sio://127.0.0.1:5000/")
    sio = window.io.connect('localhost:5000/')
    # bind functions to web socket events
    sio.on('connect', on_open)
    sio.on('connected', on_connected)
    sio.on('test', on_message)
    sio.on('disconnect', on_close)
    sio.on('connections', renderConnections)


@ bind('#btn-send', 'click')
def send(ev):
    data = document["data"].value
    if data:
        sio.emit('test', data)


@ bind('#btn-disconnect', 'click')
def close_connection(ev):
    sio.close()
    document['btn-connect'].disabled = False
