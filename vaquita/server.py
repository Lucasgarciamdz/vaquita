# server.py
import socketserver
import json
import threading
from controllers.checking_account_ctrl import CheckingAccountController
from controllers.readyz_ctrl import ReadyzController
from controllers.user_ctrl import UserController
import logging


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MainServer(socketserver.StreamRequestHandler):
    client_ips = set()
    connected_clients = {}
    client_count = 0

    def setup(self):
        super().setup()
        self.controllers = {
            "/readyz": ReadyzController(),
            "/users": UserController(),
            "/checking_accounts": CheckingAccountController(),
        }
        client_ip = self.client_address[0]
        self.accounts = set()
        MainServer.client_count += 1
        MainServer.client_ips.add(client_ip)
        logging.info(
            f"Client connected: {client_ip}. Total connected clients: {MainServer.client_count}"
        )

    def find_controller(self, path):
        for prefix, controller in self.controllers.items():
            if path.startswith(prefix):
                return controller
        return None

    def finish(self):
        super().finish()
        client_ip = self.client_address[0]
        MainServer.client_count -= 1
        MainServer.client_ips.remove(client_ip)
        logging.info(
            f"Client disconnected: {client_ip}. Total connected clients: {MainServer.connected_clients}"
        )
        for account_id in self.accounts:
            if account_id in MainServer.connected_clients:
                MainServer.connected_clients[account_id].remove(self)
                if not MainServer.connected_clients[account_id]:
                    del MainServer.connected_clients[account_id]

    def handle(self):
        # Start a new thread for reading messages
        self.read_thread = threading.Thread(target=self.handle_read)
        self.read_thread.start()
        self.read_thread.join()  # Wait for the thread to complete

    def handle_read(self):
        try:
            while True:
                request_line = self.rfile.readline().decode().strip()
                if not request_line:
                    break

                method, path, version = request_line.split(" ")
                logging.info(
                    f"Incoming request: {method} {path} from {self.client_address[0]}"
                )

                headers = self.read_headers()
                content_length = int(headers.get("Content-Length", 0))
                body = (
                    self.rfile.read(content_length).decode() if content_length else ""
                )

                controller = self.find_controller(path)
                self.request_id = json.loads(body).get("request_id")

                if controller:
                    if method == "GET":
                        controller.do_GET(self, path, headers, body)
                    elif method == "POST":
                        controller.do_POST(self, path, headers, body)
                else:
                    self.send_response(404, "Not Found")
                    self.end_headers()
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            self.send_response(500, f"Internal Server Error: {e}")
            self.end_headers()

    def send_response(self, status_code, message="", body=""):
        if self.request_id:
            body_data = json.loads(body) if body else {}
            body_data = {"request_id": self.request_id, "data": body_data}
            body = json.dumps(body_data)
        response_line = f"HTTP/1.1 {status_code} {message}\r\n"
        headers = f"Content-Type: application/json\r\nContent-Length: {len(body.encode('utf-8'))}\r\n\r\n"
        self.wfile.write(response_line.encode() + headers.encode() + body.encode())
        logging.info(f"Response sent: {status_code} {message}")
        self.wfile.flush()

    def read_headers(self):
        headers = {}
        while True:
            header_line = self.rfile.readline().decode().strip()
            if header_line == "":
                break
            key, value = header_line.split(": ", 1)
            headers[key] = value
        return headers

    def send_header(self, key, value):
        self.wfile.write(f"{key}: {value}\r\n".encode())

    def end_headers(self):
        self.wfile.write("\r\n".encode())
        self.wfile.flush()


if __name__ == "__main__":
    HOST, PORT = "localhost", 22229
    print(f"Server started on {HOST}:{PORT}")
    with ThreadedTCPServer((HOST, PORT), MainServer) as server:
        server.serve_forever()
