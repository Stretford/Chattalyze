import socket
import select
import Queue
import json
import DB
import hashlib, time

__author__ = 'stretford'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('127.0.0.1', 8888))
user_connections = {}

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
    pending_msg = {}

    while True:
        print 'waiting for next event...'
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        if not (readable or writable or exceptional):
            print "time out"
            break

        for s in readable:
            print "s:", s
            if s is server:
                connection, client_address = server.accept()
                print "connection from ", client_address
                connection.setblocking(0)
                #connection.send('ready for connection')
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print "received:", data, "from ", s.getpeername()
                    decode = json.loads(data)
                    function = decode['function']
                    if function == 'login':
                        username = decode['username']
                        password = decode['password']
                        userID = DB.verify(username, password)
                        if username and password and userID > 0:
                            print "'", username, "' logged in from ", s.getpeername()
                            token = hashlib.md5(str(time.time())).hexdigest()
                            user_connections[str(userID)] = (s, token)
                            friends = DB.get_friends(userID)
                            reply = {'function': 'token', 'token': token, 'friends': friends}
                            s.send(json.dumps(reply))
                    elif function == 'send':
                        received = decode['token']
                        token_received = received.split('_')[0]
                        userid_received = received.split('_')[2]
                        username_received = received.split('_')[1]
                        if user_connections[str(userid_received)][1] != token_received:
                            s.send('authentication failed')
                        else:
                            to = str(decode['to'])
                            msg = decode['msg']
                            print "user_connections:", user_connections
                            if to and to in user_connections:
                                data = {"from": username_received, "to": to, "msg": msg}
                                conn = user_connections[to][0]
                                conn.send(json.dumps(data))
                                print "transferring ", msg, " to ", conn.getpeername()
                            else:
                                if to in pending_msg:
                                    pending_msg[to].append(msg)
                                else:
                                    pending_msg[to] = [msg]
                            s.send('success')
                            print "pending messages: ", pending_msg

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
run()
