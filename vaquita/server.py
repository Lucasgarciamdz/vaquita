import socketserver
import json
from controllers.readyz_ctrl import ReadyzController
from controllers.user_ctrl import UserController
import logging


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MainServer(socketserver.StreamRequestHandler):
    connected_clients = 0
    client_ips = set()

    def __init__(self, *args, **kwargs):
        self.path = None
        self.headers = None
        self.body = None
        self.controllers = {
            '/readyz': ReadyzController(),
            '/users': UserController(),
        }
        super().__init__(*args, **kwargs)
        client_ip = self.client_address[0]
        MainServer.connected_clients += 1
        MainServer.client_ips.add(client_ip)
        logging.info(f"Client connected: {client_ip}. Total connected clients: {MainServer.connected_clients}")

    def find_controller(self, path):
        for prefix, controller in self.controllers.items():
            if path.startswith(prefix):
                return controller
        return None

    def handle(self):
        try:
            request_line = self.rfile.readline().decode().strip()
            if not request_line:
                return

            method, path, version = request_line.split(' ')
            self.path = path
            logging.info(f"Incoming request: {method} {path} from {self.client_address[0]}")

            headers = self.read_headers()
            self.headers = headers

            content_length = int(headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode() if content_length else ''
            self.body = body

            controller = self.find_controller(path)

            if controller:
                if method == 'GET':
                    controller.do_GET(self)
                elif method == 'POST':
                    controller.do_POST(self)
            else:
                self.send_response(404, 'Not Found')
                self.end_headers()

            # if headers.get("Connection", "").lower() == "close":
            #     self.finish()
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            self.send_response(500, f'Internal Server Error: {e}')
            self.end_headers()


    # def finish(self):
    #     super().finish()
    #     client_ip = self.client_address[0]
    #     MainServer.connected_clients -= 1
    #     MainServer.client_ips.remove(client_ip)

    def read_headers(self):
        headers = {}
        while True:
            header_line = self.rfile.readline().decode().strip()
            if header_line == '':
                break
            key, value = header_line.split(': ', 1)
            headers[key] = value
        return headers

    def send_response(self, status_code, message):
        self.wfile.write(f"HTTP/1.1 {status_code} {message}\r\n".encode())

    def send_header(self, key, value):
        self.wfile.write(f"{key}: {value}\r\n".encode())

    def end_headers(self):
        self.wfile.write("\r\n".encode())


if __name__ == "__main__":
    HOST, PORT = 'localhost', 22229
    print(f"Server started on {HOST}:{PORT}")
    with ThreadedTCPServer((HOST, PORT), MainServer) as server:
        server.serve_forever()