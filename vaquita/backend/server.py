# server.py
import socket
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

    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        bind_and_activate=True,
        address_family=socket.AF_INET,
    ):
        self.address_family = address_family
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MainServer(socketserver.StreamRequestHandler):
    client_count = 0
    connected_clients = {}
    connected_clients_lock = threading.Lock()

    def setup(self):
        super().setup()
        self.controllers = {
            "/readyz": ReadyzController(),
            "/users": UserController(),
            "/checking_accounts": CheckingAccountController(),
        }
        client_ip = self.client_address[0]
        MainServer.client_count += 1
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
        with MainServer.connected_clients_lock:
            uuid_to_remove = None
            print(f"Connected clients: {MainServer.connected_clients}")
            print(f"Client IP: {client_ip}")
            print(self)
            for uuid_key, client_info in MainServer.connected_clients.items():
                if client_info["ip"] == client_ip and client_info["handler"] == self:
                    uuid_to_remove = uuid_key
                    break
            if uuid_to_remove:
                del MainServer.connected_clients[uuid_to_remove]
                MainServer.client_count -= 1
                logging.info(
                    f"Client disconnected: {client_ip} (UUID: {uuid_to_remove}). Total connected clients: {MainServer.client_count}"
                )
            else:
                logging.warning(
                    f"Failed to find a connected client with IP: {client_ip}"
                )

    def handle(self):
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
    HOST, PORT = (
        "0.0.0.0",
        22229,
    )  # Use "0.0.0.0" for IPv4 or "::" for IPv6 to listen on all interfaces
    try:
        addr_info = socket.getaddrinfo(
            HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        )
        addr_family = addr_info[0][0]  # Get address family based on the host

        print(f"Server starting on {HOST}:{PORT} with address family {addr_family}")
        with ThreadedTCPServer(
            (HOST, PORT), MainServer, address_family=addr_family
        ) as server:
            server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")
