__author__ = 'stretford'

import socket, select, sys


def ds_asyncore(addr, callback, msg, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.send(msg)
    r, w, e = select.select([s], [], [], timeout)
    if r:
        respose_data = s.recv(1024)
        callback(respose_data)
        s.close()
        return 0
    else:
        s.close()
        return 1