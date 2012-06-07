tornado-zmq-sockjs-example
==========================

Example of a application, which uses [Tornado](http://www.tornadoweb.org) web-server for backend side,
    [SockJS](http://sockjs.org) for client communications and [ØMQ](http://www.zeromq.org/bindings:python) for inner communications.

Installation
------------

1. Clone this repository

    `git clone git://github.com/svartalf/tornado-zmq-sockjs-example.git`

2. Install required libraries

    `pip install -r requirements.txt`

3. Run server with a command

    `python main.py`

4. Open your browser:

    `http://localhost:8080`

Pitfalls
--------

**Do not save** instances of the ZMQ sockets in the connection, this will cause memory leaks!
Save instances of the `ZMQStream` only.

Wrong way:

    class SocketConnection(sockjs.tornado.SockJSConnection):

        def __init__(self, *args, **kwargs):
            context = zmq.Context()
            self.publisher = context.socket(zmq.PUB)
            self.publisher.bind(IPC_SOCKET)
            self.publish_stream = ZMQStream(publisher)

Good way:

    class SocketConnection(sockjs.tornado.SockJSConnection):

        def __init__(self, *args, **kwargs):
            context = zmq.Context()
            publisher = context.socket(zmq.PUB)  # Notice `self' lack
            publisher.bind(IPC_SOCKET)
            self.publish_stream = ZMQStream(publisher)


Links
-----

See official ZMQ documentation for using Tornado with PyZMQ: http://zeromq.github.com/pyzmq/eventloop.html