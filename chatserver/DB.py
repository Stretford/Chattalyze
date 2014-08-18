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
    for row in rows.fetchall():
        d = json.loads(row[0])
        d['token'] = num
        result.append(d)
        num += 1
    conn.close()
    return result


def execute(sqlstr):
    conn = sqlite3.connect("chatserver.sqlite")
    cu = conn.cursor()
    cu.execute(sqlstr)
    conn.commit()
    conn.close()


