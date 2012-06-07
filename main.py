# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import sockjs.tornado
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

# Install ZMQ ioloop instead of a tornado ioloop
# http://zeromq.github.com/pyzmq/eventloop.html
ioloop.install()

# Socket for communication between sockets
IPC_SOCKET = 'ipc:///tmp/zmq.ipc.sock'


class IndexHandler(tornado.web.RequestHandler):
    """Template renderer"""

    def get(self, *args, **kwargs):
        self.render('index.html')


class SocketConnection(sockjs.tornado.SockJSConnection):

    clients = set()

    def on_open(self, request):
        self.clients.add(self)

        context = zmq.Context()

        publisher = context.socket(zmq.PUB)
        publisher.bind(IPC_SOCKET)

        self.publish_stream = ZMQStream(publisher)

        subscriber = context.socket(zmq.SUB)
        subscriber.connect(IPC_SOCKET)
        subscriber.setsockopt(zmq.SUBSCRIBE, '')

        self.subscribe_stream = ZMQStream(subscriber)
        self.subscribe_stream.on_recv(self.on_receive_message)

    def on_message(self, message):
        self.publish_stream.send_unicode(message)

    def on_receive_message(self, message):
        self.send(message)

    def on_close(self):
        self.clients.remove(self)

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    SocketRouter = sockjs.tornado.SockJSRouter(SocketConnection, '/socket')

    app = tornado.web.Application(
        [(r'/', IndexHandler), ] + SocketRouter.urls,
        debug=True,
        autoreload=True,
    )

    app.listen(8080)

    tornado.ioloop.IOLoop.instance().start()
