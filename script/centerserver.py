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
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            msg = wsock.receive()
            if msg is not None:  
                if msg == 'game_start|': 
                    retMsg = 'game_ready|ok'
                elif '|' in msg:
                    cmdArr = msg.split('|', 1)
                    retMsg = 'you press ' + cmdArr[0]
                else:
                    retMsg = 'unsupport'

                if retMsg is not None:
                    wsock.send(retMsg)
            else: break

        except WebSocketError:
            break
 
server = WSGIServer(("0.0.0.0", 8888), app, handler_class=WebSocketHandler)
server.serve_forever()


"""
from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        def data_provider():
            for i in range(1, 200, 25):
                yield "#" * i

        self.send(data_provider())

        for i in range(0, 200, 25):
            print i
            self.send("*" * i)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m
        if len(m) == 175:
            self.close(reason='Bye bye')

if __name__ == '__main__':
    try:
        ws = DummyClient('ws://localhost:9000/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
   """