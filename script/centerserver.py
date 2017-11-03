#!/usr/bin/env python
#coding=utf-8
"""
    pip install bottle
    pip install websocket-client
    pip install bottle-websocket
"""

from bottle import request, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import websocket
import threading

import gevent

app = Bottle()
@app.route('/websocket')
def handle_websocket():
    retMsg = None
    ClientSock = None
    ServerSock = request.environ.get('wsgi.websocket')

    if not ServerSock:
        abort(400, 'Expected WebSocket request.')
    else:
        ServerSock.send('connected Center Server')
    while True:
        try:
            msg = ServerSock.receive()
            if msg is not None:  
                if '|' in msg:
                    cmdArr = msg.split('|', 1)

                    if cmdArr[0] == 'connect':

                        
                        def on_message(ws, message):
                            ServerSock.send(message)

                        def on_close(ws):
                            print "### closed ###"

                        websocket.enableTrace(True)
                        ClientSock = websocket.WebSocketApp("ws://127.0.0.1:8899/websocket", on_message = on_message, on_close = on_close)
                        wst = threading.Thread(target=ClientSock.run_forever)
                        wst.daemon = True
                        wst.start()
                        
                        print('connected client')
                        
                    else:
                        if ClientSock is None:
                            ServerSock.send('error|notConnectClient')
                            break
                        else:
                            ClientSock.send(msg)                            
                else:
                    retMsg = 'unsupport'

                if retMsg is not None:
                    ServerSock.send(retMsg)
            else:
                print 'bbb'
                ServerSock.send('error|empty')

        except WebSocketError:
            break
 
server = WSGIServer(("0.0.0.0", 8888), app, handler_class=WebSocketHandler)
server.serve_forever()