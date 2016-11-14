# -*- coding: utf-8 -*-
# author: Vasenkov Stanislav
# skype: police_1771
# telegram: @iTerkin
#
# simple client-server project to control virtual-machine with server
# server.py: can send requests to client to interact with interfaces and update client
# client.py: can interact with OS (google it: flask), /cmd/ as example
#            can update itself

import os
import codecs
import shutil
import socket

from flask import Flask, request


app = Flask(__name__)
LOCAL_DIR = 'C:/vm/'
CLIENT_NAME = 'client.py'


@app.route("/")
def index():
    message = 'virtual machine ip: %s' % socket.gethostbyname(socket.gethostname())
    return message


# some interface for working with command line
@app.route('/cmd/')
def cmd():
    some_arg = request.args.get('some_arg')
    print some_arg

    # for example
    os.system(r'' + 'ipconfig')

    message = 'SUCCESS (cmd): script launched'
    print message
    return message


@app.route('/update_client/')
def update_client():
    server_folder_ = request.args.get('server_folder')
    server_folder = server_folder_.replace('::slash::', '\\')

    if not os.path.exists(server_folder):
        message = 'remote directory was not found, ' + server_folder
        print message
        return message

    try:
        server_folder_list = os.listdir(server_folder)
        for file_name in server_folder_list:

            # 1. Rewrite server_vm.py (it will restarted by watchdog)
            if file_name == CLIENT_NAME:
                remote_server = codecs.open(server_folder + CLIENT_NAME, 'r')
                content = remote_server.read()
                content = unicode(content, 'utf-8')
                remote_server.close()

                local_server = codecs.open(LOCAL_DIR + CLIENT_NAME, 'w', 'utf-8')
                local_server.write(content)
                local_server.close()

            # 2. Copy other files in folder (if they are)
            else:
                shutil.copy2(server_folder + file_name, LOCAL_DIR + file_name)

        message = 'python-server and files are updated'
        print message
        return message

    except Exception, error:
        message = 'cant update, ' + str(error)
        print message
        return message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

# Sometimes, when update_client works and rewrites client.py on local vm, it cuts some symbols at the end of page

# app.run(host="0.0.0.0", port=80, debug=True)
# to
# app.run(host="0.0.0.0",

# and server falls when watchdog restarts it.
# I don't know how to fix this bug, so i added big comment (with #) to the end of page.

# P.S. i dream, when i fix the bug and comment will be deprecated, i'll leave it because it's funny
