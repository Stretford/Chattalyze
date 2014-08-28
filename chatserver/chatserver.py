import socket
import select
import Queue
import json
import DB
import hashlib, time, base64

__author__ = 'stretford'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('127.0.0.1', 8888))
user_connections = {}
PENDING_MSG = {}      #{'to_id': [{'from_id'|'from_name'|'msg'}, {...}]}
TOKEN = {}
USERS = DB.get_users()
CONNECTIONS = []

'''
def send_data(addr, msg, sender, receiver):
    try:
        server.connect(addr)
    except Exception, e:
        if receiver in user_connections:
            del user_connections[receiver]
            print Exception, ":", e
    else:
        data = {"from": sender, "to": receiver, "msg": msg}
        server.send(json.dumps(data))
'''


def run():
    server.listen(5)
    inputs = [server]
    outputs = []
    message_queues = {}

    while True:
        #print 'waiting for next event...'
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        if not (readable or writable or exceptional):
            print "time out"
            break

        for s in readable:
            if s is server:
                connection, client_address = server.accept()
                print "connection from ", client_address
                connection.setblocking(0)
                #connection.send('ready for connection')
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()

            else:
                transfer_message(s)

                data = s.recv(1024)
                if data:
                    print "received:", data, "from ", s.getpeername()
                    try:
                        decode = json.loads(data)
                        print "json loaded:", decode
                    except:
                        if not s.getpeername() in CONNECTIONS:
                            handshake(s, data)
                            CONNECTIONS.append(s.getpeername())
                        else:
                            raw_data = parse_data(data)
                            print "parsed:", raw_data
                            s.send(encaps_data('test from server'))
                            #s.send(encaps_data(raw_data))
                        continue
                    function = decode['function']

                    if function == 'login':
                        username = decode['username']
                        password = decode['password']
                        userID = DB.verify(username, password)
                        if username and password and userID > 0:
                            print "'", username, "' logged in from ", s.getpeername()
                            token = hashlib.md5(str(time.time())).hexdigest()
                            TOKEN[str(userID)] = token
                            friends = DB.get_friends(userID)
                            reply = {'function': 'token', 'token': token, 'friends': friends}
                            s.send(json.dumps(reply))

                    elif function == 'appendADDR':
                        token = decode['token']
                        token_received = token.split('_')[0]
                        userid_received = token.split('_')[2]
                        if TOKEN[str(userid_received)] != token_received:
                            s.send('authentication failed')
                        else:
                            sending_addr = (decode['addr'][0], decode['addr'][1])
                            user_connections[str(userID)] = sending_addr

                    elif function == 'send':
                        token = decode['token']
                        token_received = token.split('_')[0]
                        userid_received = token.split('_')[2]
                        username_received = token.split('_')[1]
                        to = str(decode['to'])
                        to_token_received = decode['to_token']
                        to_token = USERS[to][1]
                        print to_token, to_token_received
                        if TOKEN[str(userid_received)] != token_received or to_token != to_token_received:
                            s.send('authentication failed')
                        else:
                            msg = decode['msg']
                            temp = {'from_id': userid_received, 'from_name': username_received, 'msg': msg}
                            if to in PENDING_MSG:
                                PENDING_MSG[to].append(temp)
                            else:
                                PENDING_MSG[to] = [temp]
                            print "pending messages: ", PENDING_MSG

                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    #pass

                    print "closing ", client_address
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    #s.close()
                    del message_queues[s]

        for s in writable:
            transfer_message(s)
            '''
            try:
                next_msg = message_queues[s].get_nowait()
                #next_msg = ''
            except Queue.Empty:
                print s.getpeername(), ' queue empty'
                outputs.remove(s)
            else:
                print "sending ", next_msg, " to ", s.getpeername()

                #s.send(next_msg)

        for s in exceptional:
            print "exception condition on ", s.getpeername()
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
            '''
    '''
        while True:
            data = connection.recv(1024)
            if not data:
                break

            connection.send(data)
    connection.close()
    sock.close()
    '''

def transfer_message(s):
    if PENDING_MSG.items().__len__() > 0:
                for k, v in user_connections.items():
                    if v[0] == s.getpeername()[0] and v[1] == s.getpeername()[1]:
                        if k in PENDING_MSG:
                            pm = PENDING_MSG[k]
                            for msg in pm:
                                temp = json.dumps({'senderid': msg['from_id'], 'sendername': msg['from_name'], 'msg': msg['msg']})
                                s.send(temp)
                                print "sending ", temp, " to ", s.getpeername()
                            del PENDING_MSG[k]
                        else:
                            pass


def handshake(s, data):
    key = None
    if not len(data):
        return encaps_data('aa')
    for line in data.split('\r\n\r\n')[0].split('\r\n')[1:]:
        k, v = line.split(': ')
        if k == 'Sec-WebSocket-Key':
            key = base64.b64encode(hashlib.sha1(v + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
    if not key:
        return encaps_data('aa')
    response = 'HTTP/1.1 101 Switching Protocols\r\n'\
               'Upgrade: websocket\r\n'\
               'Connection: Upgrade\r\n'\
               'Sec-WebSocket-Accept:' + key + '\r\n\r\n'
    s.send(response)
    print "websocket response:", response



def parse_data(msg):
    print "before parsing:", msg
    code_length = ord(msg[1]) & 127

    if code_length == 126:
        masks = msg[4:8]
        data = msg[8:]
    elif code_length == 127:
        masks = msg[10:14]
        data = msg[14:]
    else:
        masks = msg[2:6]
        data = msg[6:]

    i = 0
    raw_str = ''

    for d in data:
        raw_str += chr(ord(d) ^ ord(masks[i%4]))
        i += 1
    return raw_str


def encaps_data(raw_str):
    back_str = []

    back_str.append('\x81')
    data_length = len(raw_str)

    if data_length < 125:
        back_str.append(chr(data_length))
    else:
        back_str.append(chr(126))
        back_str.append(chr(data_length >> 8))
        back_str.append(chr(data_length & 0xFF))

    back_str = "".join(back_str) + raw_str
    return back_str

run()
