import socketserver
from controllers.readyz_ctrl import ReadyzController
from controllers.user_ctrl import UserController


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class MainServer(socketserver.StreamRequestHandler):
    def __init__(self, *args, **kwargs):
        self.path = None
        self.headers = None
        self.body = None
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

    def handle(self):
        while True:
            try:
                # Read the request line
                request_line = self.rfile.readline().decode().strip()
                if not request_line:
                    break  # No more data from the client

                method, path, version = request_line.split(' ')

                # Read headers
                headers = {}
                while True:
                    header_line = self.rfile.readline().decode().strip()
                    if header_line == '':
                        break
                    key, value = header_line.split(': ', 1)
                    headers[key] = value
                self.headers = headers

                # Read the body, if any
                content_length = int(headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode() if content_length else ''
                print(f"Received body:\n{body}")  # Debug statement
                self.body = body

                # Find the appropriate controller
                controller = self.find_controller(path)
                self.path = path

                # Handle the request
                if controller:
                    if method == 'GET':
                        controller.do_GET(self)
                    elif method == 'POST':
                        controller.do_POST(self)
                else:
                    self.send_response(404)
                    self.end_headers()

                # Check if the connection should be closed
                if headers.get("Connection", "").lower() == "close":
                    break
            except Exception as e:
                print(f"Exception during request handling: {e}")

    def send_response(self, status_code):
        self.wfile.write(f"HTTP/1.1 {status_code} {'OK' if status_code == 200 else 'Not Found'}\r\n".encode())

    def send_header(self, key, value):
        self.wfile.write(f"{key}: {value}\r\n".encode())

    def end_headers(self):
        self.wfile.write("\r\n".encode())


if __name__ == "__main__":
    HOST, PORT = 'localhost', 22229
    print(f"Server started on {HOST}:{PORT}")
    with ThreadedTCPServer((HOST, PORT), MainServer) as server:
        server.serve_forever()
