from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from server.handlers.log import LogHandler, LogViewHandler, LogViewFileHandler, HomeHandler
import os

define('port', default=8888, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    settings = dict(
        template_path=os.path.abspath(os.getcwd() + "/server/templates"),
        debug=True
    ) 

    app = Application([
        ("/log/view/dataload/(?P<path>\w*.txt)", LogViewFileHandler),
        (r"/log/view/dataload", LogViewHandler), 
        ("/log/view", LogHandler),
        ("/", HomeHandler),
    ], **settings)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()