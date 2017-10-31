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
from ws4py.client.threadedclient import WebSocketClient


app = Bottle()
@app.route('/websocket')
def handle_websocket():
    serversock = request.environ.get('wsgi.websocket')
    if not serversock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            msg = serversock.receive()
            if msg is not None:  
                if '|' in msg:
                    cmdArr = msg.split('|', 1)
					if cmdArr[0] == 'connect':
						try:
							clientSock = WebSocketClient('ws://127.0.0.1:8989/websocket', protocols=['http-only', 'chat'])
							clientSock.connect()
							clientSock.send('connect|')
						except WebSocketError:
							clientSock.close()
							print 'connect client error' 
							
					else
						if clientSock is None:
							break
						else:
							clientSock.send(msg)
							while True:
								try:
									cmsg = clientSock.receive()
									retMsg = cmsg
								except WebSocktError:
									break
                else:
                    retMsg = 'unsupport'

                if retMsg is not None:
                    serversock.send(retMsg)
            else: break

        except WebSocketError:
            break
 
server = WSGIServer(("0.0.0.0", 8888), app, handler_class=WebSocketHandler)
server.serve_forever()