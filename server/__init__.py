from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from server.views import TestHandler
from server.handlers.log import LogHandler, LogViewHandler
import os

define('port', default=8888, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    settings = dict(
        template_path=os.path.abspath(os.getcwd() + "/server/templates"),
        debug=True
    ) 

    app = Application([
        ("/", TestHandler),
        ("/log/view", LogHandler),
        (r"/log/view/dataload", LogViewHandler), 
    ], **settings)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()