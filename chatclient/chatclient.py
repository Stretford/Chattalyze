from flask import Flask, render_template, request, redirect, url_for
import asyn
import socket
import json
import select

app = Flask(__name__)
LOGGER = {}
FRIENDS = []
TOKEN = ''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        addr = ('localhost', 8888)
        username = request.form['username']
        password = request.form['password']
        data = {'function': 'login', 'username': username, 'password': password}
        data = json.dumps(data)
        temp = asyn.ds_asyncore(addr, callback, data, timeout=5)
        print temp
        reply = json.loads(temp)
        print reply['function']
        global LOGGER, FRIENDS, TOKEN
        if reply['function'] == 'token':
            LOGGER['username'] = username
            FRIENDS = reply['friends']
            userid = FRIENDS[len(FRIENDS) - 1][0]
            LOGGER['userid'] = userid
            TOKEN = reply['token'] + '_' + username + '_' + str(userid)
            return 'logged in'

    html = render_template('login.html')
    return html

@app.route('/index', methods=['GET', 'POST'])
def index():
    print "TOKEN:", FRIENDS
    html = render_template('index.html', friends=FRIENDS, logger=LOGGER, token=TOKEN)
    return html


def callback(response_data):
    print response_data

if __name__ == '__main__':
    app.run(debug=True, port=7777)

