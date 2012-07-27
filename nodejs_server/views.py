import websocket
from urllib2 import urlopen

def handshake(host, port):
    u = urlopen("http://%s:%d/socket.io/1/" % (host, port))
    if u.getcode() == 200:
        response = u.readline()
        (sid, hbtimeout, ctimeout, supported) = response.split(":")
        supportedlist = supported.split(",")
        if "websocket" in supportedlist:
            return (sid, hbtimeout, ctimeout)
        else:
            raise TransportException()
    else:
        raise InvalidResponseException()

def connect_to_nodejs(host = "localhost", port = 5555):
    HOSTNAME = host
    PORT = port
    sid = 0
    try:
        (sid, hbtimeout, ctimeout) = handshake(HOSTNAME, PORT) #handshaking according to socket.io spec.
    except Exception as e:
        print e
        pass
    ws = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (HOSTNAME, PORT, sid))
    return ws

def send_message(event, message):
    ws = connect_to_nodejs(host="192.168.0.168")
    print(message)
#    ws.send('2::')
#    ws.send('5:1::{"name":"test", "args":[{"user":"server"}]}')

    string_to_send = '5:1::{"name":"' + event + '", "args":[{' + message + '}]}'
    print(string_to_send)

    ws.send('2::')
    ws.send(string_to_send)
    ws.close()