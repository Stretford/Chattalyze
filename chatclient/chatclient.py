from flask import Flask, render_template, request, redirect, url_for, jsonify
import asyn
import socket
import json, time
import select, thread

app = Flask(__name__)
LOGGER = {}
FRIENDS = []
TOKEN = ''
RECEIVED_DATA = []
ADDR = ('localhost', 8888)
LOCAL_RECEIVING_PORTAL = ()

@app.route('/', methods=['GET', 'POST'])
def login():
    global LOCAL_RECEIVING_PORTAL
    if request.method == 'POST':
        #local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        username = request.form['username']
        password = request.form['password']

        data = {'function': 'login', 'username': username, 'password': password}
        data = json.dumps(data)
        print data
        temp = asyn.ds_asyncore(ADDR, callback, data, timeout=5)
        print temp
        reply = json.loads(temp)
        print reply
        global LOGGER, FRIENDS, TOKEN
        if reply['function'] == 'token':
            #thread.start_new_thread(asyn_receive, (local_socket, ''))
            LOGGER['username'] = username
            FRIENDS = reply['friends']
            userid = FRIENDS[-1][0]
            LOGGER['userid'] = userid
            TOKEN = reply['token'] + '_' + username + '_' + str(userid)
            thread.start_new_thread(asyn_receive, (TOKEN, ''))
            return 'logged in'

    html = render_template('login.html')
    return html

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print 'here'
        msg = request.form['msg']
        to = request.form['to']
        to_token = request.form['to_token']
        data = {'function': 'send', 'token': TOKEN, 'msg': msg, 'to': to, 'to_token': to_token}
        data = json.dumps(data)
        print "before sending:", data
        temp = asyn.ds_asyncore(ADDR, callback, data, timeout=5)
        print(temp)
        return temp

    html = render_template('index.html', friends=FRIENDS, logger=LOGGER, token=TOKEN)
    return html

@app.route('/receive_msg')
def receive_msg():
    return "Stretford_hello!"
    #return render_template('test.html')


def asyn_receive(token, useless):
    global LOCAL_RECEIVING_PORTAL
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDR)
    msg = {"function": "appendADDR", "addr": s.getsockname(), "token": token}
    s.send(json.dumps(msg))
    print "listening at:", s.getsockname()
    aaa = True
    while aaa:
        data = s.recv(1024)
        if data:
            RECEIVED_DATA.append(data)
            print "received from server:", data




def callback(response_data):
    print response_data


if __name__ == '__main__':
    app.run(debug=True, port=7777)

