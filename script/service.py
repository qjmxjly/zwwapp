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


app = Bottle()
@app.route('/websocket')

def handle_websocket():
    ServerSock = request.environ.get('wsgi.websocket')
    if not ServerSock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            msg = ServerSock.receive()
            if msg is not None:  
                if '|' in msg:
                    cmdArr = msg.split('|', 1)
                    if cmdArr[0] == 'game_start':
                        retMsg = 'game_ready|ok'
                    else:
                        retMsg = 'you pressed ' + cmdArr[0]
                else:
                    retMsg = 'unsupport'

                if retMsg is not None:
                    ServerSock.send(retMsg)
            else: break

        except WebSocketError:
            break


server = WSGIServer(("0.0.0.0", 8899), app, handler_class=WebSocketHandler)
server.serve_forever()