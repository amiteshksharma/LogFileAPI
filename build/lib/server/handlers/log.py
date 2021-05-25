from tornado.web import RequestHandler

class LogHandler(RequestHandler):
    """Print 'Hello, world!' as the response body."""

    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.render("home.html")