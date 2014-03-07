from wsgiref.simple_server import (
    WSGIServer,
    WSGIRequestHandler,
    ServerHandler,
)

class CalculatorServerHandler(ServerHandler):

    def run(self, application):
        """Invoke the application"""
        # Note to self: don't move the close()!  Asynchronous servers shouldn't
        # call close() from finish_response(), so if you close() anywhere but
        # the double-error branch here, you'll break asynchronous servers by
        # prematurely closing.  Async servers must return from 'run()' without
        # closing if there might still be output to iterate over.
        self.setup_environ()
        self.result = application(self.environ, self.start_response)
        self.finish_response()

    def handle_error(self):
        pass


class CalculatorWSGIHandler(WSGIRequestHandler):

    def handle(self):
        """Handle a single HTTP request"""

        # copy-pasta from wsgireg so we can use our braindead handler

        self.raw_requestline = self.rfile.readline()
        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = CalculatorServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


class CalculatorServer(WSGIServer):

    def handle_error(self, request, client_address):
        raise
