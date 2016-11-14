# author: Vasenkov Stanislav
# skype: police_1771
# telegram: @iTerkin

Some scripts for qa
1. python-selenium/download_testcomplete.py
   simple selenium script: go to page, fill forms, press buttons
2. python-testcomplete/com_testexecute.py
   script for interacting with TestExecute from python flask-server via COM
   NOTE: script works only in windows, because TestComplete is win-app
3. vm-server-client/server.py, vm-server-client/client.py
   simple client-server project to control virtual-machine with server
   server.py: can send requests to client to interact with interfaces and update client
   client.py: can interact with OS (google it: flask), /cmd/ as example
              can update itself