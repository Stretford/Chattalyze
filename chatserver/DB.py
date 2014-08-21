import sqlite3
import json, hashlib, time


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
    sqlstr = "select ID, password from users where username = '" + username + "'"
    print sqlstr
    result = query(sqlstr)
    if result.__len__() == 0:
        return -1
    psw = result[0][1]
    id = result[0][0]
    if psw == password:
        return id
    return -1


def get_friends(user):
    sqlstr = "select id,username,token from users where id in(select user1 from relations where user2 = " + str(user) + " union select user2 from relations where user1 = " + str(user) + ")"
    result = query(sqlstr)
    tmp = json.dumps(result[0])
    #result = json.loads(tmp)
    result.append((user, user))
    return result


def get_users():
    ds = query("select * from users")
    #ds = json.loads(json.dumps(ds[0]))
    result = {}
    for row in ds:
        result[str(row[0])] = (row[1], row[3])
    return result



v = (u'127.0.0.1', 56955)
c = ('127.0.0.1', 56958)
print get_users()



