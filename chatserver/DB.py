import sqlite3
import json


__author__ = 'Stretford'


def insert(sqlstr):
    conn = sqlite3.connect("chatserver.sqlite")
    cu = conn.cursor()

    cu.execute(sqlstr)
    conn.commit()
    conn.close()


def query(sqlstr):
    conn = sqlite3.connect("chatserver.sqlite")
    cu = conn.cursor()
    result = []
    rows = cu.execute(sqlstr)
    num = 0
    return rows.fetchall()


def execute(sqlstr):
    conn = sqlite3.connect("chatserver.sqlite")
    cu = conn.cursor()
    cu.execute(sqlstr)
    conn.commit()
    conn.close()


def verify(username, password):
    str = "select password from users where username = '" + username + "'"
    result = query(str)
    if result.__len__() == 0:
        return False
    result = query(str)[0][0]
    if result == password:
        return True
    return False


#print(verify('', 'abc123'))


