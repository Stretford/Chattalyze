__author__ = 'stretford'

import socket, select, sys
import json



def ds_asyncore(addr, callback, msg, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.send(msg)
    r, w, e = select.select([s], [], [], timeout)
    if r:
        respose_data = s.recv(1024)
        if respose_data == 'ready for connection':
            msg = {'function': 'login', 'username': 'sam', 'password': 'abc123'}
            msg = json.dumps(msg)
            s.send(msg)
        elif respose_data == '1':
            pass
        #callback(respose_data)
        s.close()
        return respose_data
    else:
        s.close()
        return ''

