# -*- coding: utf-8 -*-
# author: Vasenkov Stanislav
# skype: police_1771
# telegram: @iTerkin
#
# simple client-server project to control virtual-machine with server
# server.py: can send requests to client to interact with interfaces and update client
# client.py: can interact with OS (google it: flask), /cmd/ as example
#            can update

import socket
import requests
from flask import Flask


app = Flask(__name__)


# change to yours
SERVER_FOLDER = '\\\\qa_server\\'
CLIENT_IP = '192.168.0.*'


@app.route("/")
def index():
    message = 'server ip: %s' % socket.gethostbyname(socket.gethostname())
    return message


@app.route('/some_interface/')
def some_interface():
    try:
        params = {'some_arg': 'Hello, mord!'}
        url = 'http://' + CLIENT_IP + ':80/cmd/'
        do_request = requests.get(url, params=params, timeout=10)

        message = 'SUCCESS (some_interface): request sent to %s, %s' % (CLIENT_IP, do_request.text)

    except Exception, error:
        message = 'ERROR (some_interface): no connection, request sent to %s, %s' % (CLIENT_IP, error)

    print message
    return message


@app.route('/update_client/')
def update_client():
    server_folder = SERVER_FOLDER.replace('\\', '::slash::')

    try:
        params = {'host_folder_vm': server_folder}
        url = 'http://' + CLIENT_IP + '/update_vm/'
        do_request = requests.get(url, params=params, timeout=10)

        message = 'SUCCESS (update_client): request sent to %s, %s' % (CLIENT_IP, do_request.text)

    except Exception, error:
        message = 'ERROR (update_client): no connection, request sent to %s, %s' % (CLIENT_IP, error)

    print message
    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=120)
