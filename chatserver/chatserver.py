import socket
import select
import Queue
import json

__author__ = 'stretford'


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('127.0.0.1', 8888))
    server.listen(5)
    inputs = [server]
    outputs = []
    message_queues = {}
    timeout = 0

    while True:
        print 'waiting for next event...'
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        if not (readable or writable or exceptional):
            print "time out"
            break

        for s in readable:
            if s is server:
                connection, client_address = server.accept()
                print "connection from ", client_address
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print "received:", data, "from ", s.getpeername()
                    #print "  connection:", connection
                    decode = json.loads(data)
                    sender = decode['sender']

                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    print "closing ", client_address
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                print s.getpeername(), ' queue empty'
                outputs.remove(s)
            else:
                print "sending ", next_msg, " to ", s.getpeername()
                s.send(next_msg)

        for s in exceptional:
            print "exception condition on ", s.getpeername()
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]

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
