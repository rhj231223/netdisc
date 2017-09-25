# coding:utf-8
import websocket_views as ws

websocket_urls=[
    (r'^/messagewebsocket/$', ws.MessageWSHandler),
]