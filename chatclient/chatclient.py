from flask import Flask, render_template, request, redirect, url_for
import asyn
import socket
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    html = render_template('login.html')
    return html

@app.route('/index', methods=['GET', 'POST'])
def index():
    #addr = ('timmiige.gicp.net', 52989)
    addr = ('localhost', 8888)
    data = {'function': 'login', 'username': 'sam', 'password': 'abc123'}
    data = json.dumps(data)
    #asyn.ds_asyncore(addr, callback, 'test', timeout=5)
    asyn.ds_asyncore(addr, callback, data, timeout=5)
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect(addr)
    #sock.send('aaa')
    #sock.close()
    return 'logged in'

def callback(response_data):
    print response_data

if __name__ == '__main__':
    app.run(debug=True, port=7777)

