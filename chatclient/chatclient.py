from flask import Flask, render_template, request, redirect, url_for, jsonify
import asyn
import socket
import json, time
import select, thread

app = Flask(__name__)
LOGGER = {}
FRIENDS = []
TOKEN = ''
RECEIVED_DATA = {}  #'sender_id': [{'sender_name'|'msg'}]
SERVER_ADDR = ('localhost', 8888)
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
        temp = asyn.ds_asyncore(SERVER_ADDR, callback, data, timeout=5)
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
            #thread.start_new_thread(asyn_receive, (TOKEN, ''))
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
        temp = asyn.ds_asyncore(SERVER_ADDR, callback, data, timeout=5)
        print(temp)
        return temp

    html = render_template('index.html', friends=FRIENDS, logger=LOGGER, token=TOKEN)
    return html

@app.route('/receive_msg', methods=['GET', 'POST'])
def receive_msg():
    if request.method == 'POST':
        if RECEIVED_DATA:
            print "RECEIVED_DATA:", RECEIVED_DATA
            for k, v in RECEIVED_DATA.items():
                temp = v[0]
                #temp['sender_id'] = k
                del RECEIVED_DATA[k]
                result = k + '_' + temp['sender_name'] + '_' + temp['msg']
                print "post:", result
                return result
                '''for row in v:
                    sender_id = k
                    sender_name = row['sender_name']
                    msg = row['msg']
                    temp = json.dumps(msg)'''
    return ''


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        msg = request.form['msg']
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(SERVER_ADDR)
        msg = {"function": "send"}
        return msg
    return render_template('test.html')


@app.route('/sample')
def sample():
    return render_template('sample.html')


'''
def asyn_receive(token, useless): `
    global LOCAL_RECEIVING_PORTAL
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDR)
    msg = {"function": "appendADDR", "addr": s.getsockname(), "token": token}
    s.send(json.dumps(msg))
    print "listening at:", s.getsockname()
    aaa = True
    while aaa:
        data = s.recv(1024)
        if data:
            data = json.loads(data)
            sender_id = data['senderid']
            sender_name = data['sendername']
            msg = data['msg']
            temp = {'sender_name': sender_name, 'msg': msg}
            if not sender_id in RECEIVED_DATA:
                RECEIVED_DATA[sender_id] = [temp]
            else:
                RECEIVED_DATA[sender_id].append(temp)
'''



def callback(response_data):
    print response_data


if __name__ == '__main__':
    app.run(debug=True, port=7777)

