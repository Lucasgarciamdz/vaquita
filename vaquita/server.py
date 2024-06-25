from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from controllers.readyz_ctrl import ReadyzController
from controllers.user_ctrl import UserController


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class MainServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controllers = {
            '/readyz': ReadyzController(),
            '/users': UserController(),
        }
        super().__init__(*args, **kwargs)

    def find_controller(self, path):
        for prefix, controller in self.controllers.items():
            if path.startswith(prefix):
                return controller
        return None

    def do_GET(self):
        controller = self.find_controller(self.path)
        if controller:
            controller.do_GET(self)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        controller = self.find_controller(self.path)
        if controller:
            controller.do_POST(self)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    HOST, PORT = 'localhost', 8080
    print(f"Server started on {HOST}:{PORT}")
    server = ThreadedHTTPServer((HOST, PORT), MainServer)
    server.serve_forever()
