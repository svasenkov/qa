# author: Vasenkov Stanislav
# skype: police_1771
# telegram: @iTerkin
#
# script for interacting with TestExecute from python flask-server via COM
# NOTE: script works only in windows, because TestComplete is win-app

import os
import psutil
import socket

from flask import Flask, request

import pythoncom
import win32com.client


app = Flask(__name__)
TEST_EXECUTE_PATH = 'C:\Program Files (x86)\SmartBear\TestExecute 12\Bin\TestExecute.exe'
TEST_EXECUTE_NAME = 'TestExecute.exe'
FRAMEWORK_PATH = "C:\\Framework\\Framework.pjs"


@app.route("/")
def index():
    message = 'virtual machine ip: %s<br/>' % socket.gethostbyname(socket.gethostname())
    message += 'TestExecute is installed:' + str(os.path.exists(TEST_EXECUTE_PATH)) + '<br/>'
    message += 'TestExecute is launched:' + str(TEST_EXECUTE_NAME in [p.name() for p in psutil.process_iter()])

    return message


# you can run TC function from interface:
# host/testexecute/?script_file=NAME&function_name=NAME&some_arg_1=NAME&some_arg_2=NAME
@app.route('/testexecute/')
def testexecute():
    project_name = 'Framework'
    script_file = request.args.get('script_file')
    function_name = request.args.get('function_name')
    some_arg_1 = request.args.get('some_arg_1')
    some_arg_2 = request.args.get('some_arg_2')

    if not os.path.exists(TEST_EXECUTE_PATH):
        message = 'ERROR (testexecute): TestExecute not installed'
        print message
        return message

    if not os.path.exists(FRAMEWORK_PATH):
        message = 'ERROR (testexecute): wrong path to project, ' + FRAMEWORK_PATH
        print message
        return message

    pythoncom.CoInitialize()

    test_execute_app = win32com.client.Dispatch("TestExecute.TestExecuteApplication.12")
    integration_object = test_execute_app.Integration
    if not integration_object.IsProjectSuiteOpened():
        integration_object.OpenProjectSuite(FRAMEWORK_PATH)
        print 'Project is opened: ' + FRAMEWORK_PATH

    if integration_object.IsRunning():
        message = 'ERROR (testexecute): TestExecute is already running'
        print message
        return message

    integration_object.RunRoutineEx(project_name, script_file, function_name, [some_arg_1, some_arg_2])

    pythoncom.CoUninitialize()

    message = 'SUCCESS (testexecute): script launched'
    print message
    return message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)