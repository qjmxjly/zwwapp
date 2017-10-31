#!/usr/bin/env python
#coding=utf-8
"""
    pip install bottle
    pip install websocket-client
    pip install bottle-websocket
"""

"""from bottle import request, Bottle, abort
app = Bottle()
"""

from bottle import get, run
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

"""
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
"""

users = set()   # 连接进来的websocket客户端集合

@get('/websocket', apply=[websocket])

def Handle_WebSocket(ws):
    users.add(ws)
    while True:
        msg = ws.receive()  # 接客户端的消息
        if msg is not None:  
            if msg == 'game_start|': 
                retMsg = 'game_ready|ok'
            elif '|' in msg:
                cmdArr = msg.split('|', 1)
                retMsg = 'you press ' + cmdArr[0]
            else:
                retMsg = 'unsupport'

            if retMsg is not None:
                for u in users:
                    print type(u)
                    u.send(retMsg)
                    print u,retMsg
        else: break

    # 如果有客户端断开连接，则踢出users集合
    users.remove(ws)
run(host='0.0.0.0', port=8888, server=GeventWebSocketServer)

"""
server = WSGIServer(("0.0.0.0", 8888), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
"""
