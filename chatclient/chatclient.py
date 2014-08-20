from flask import Flask, render_template, request, redirect, url_for
import asyn
import socket
import json
import select, thread

app = Flask(__name__)
LOGGER = {}
FRIENDS = []
TOKEN = ''
TEST = ['bb']

@app.route('/', methods=['GET', 'POST'])
def login():
    thread.start_new_thread(timer, (1, 1))
    if request.method == 'POST':
        addr = ('localhost', 8888)
        username = request.form['username']
        password = request.form['password']
        data = {'function': 'login', 'username': username, 'password': password}
        data = json.dumps(data)
        temp = asyn.ds_asyncore(addr, callback, data, timeout=5)
        print temp
        reply = json.loads(temp)
        print reply
        global LOGGER, FRIENDS, TOKEN
        if reply['function'] == 'token':
            LOGGER['username'] = username
            FRIENDS = reply['friends']
            userid = FRIENDS[-1][0]
            LOGGER['userid'] = userid
            TOKEN = reply['token'] + '_' + username + '_' + str(userid)
            return 'logged in'

    html = render_template('login.html', test=TEST)
    return html

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print 'here'
        addr = ('localhost', 8888)
        msg = request.form['msg']
        to = request.form['to']
        data = {'function': 'send', 'token': TOKEN, 'msg': msg, 'to': to}
        data = json.dumps(data)
        print "before sending:", data
        temp = asyn.ds_asyncore(addr, callback, data, timeout=5)
        print(temp)
        return temp

    html = render_template('index.html', friends=FRIENDS, logger=LOGGER, token=TOKEN)
    return html


def callback(response_data):
    print response_data

def timer(no, interval):
    TEST.append('aa')

if __name__ == '__main__':
    app.run(debug=True, port=7777)

