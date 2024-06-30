import json
import socket
import threading
import uuid
from queue import Queue, Empty


class SocketClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SocketClient, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, host="localhost", port=22229):
        if self._initialized:
            return
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.lock = threading.Lock()
        self._initialized = True
        self.response_queues = {}
        self.listener_thread = threading.Thread(
            target=self.listen_for_updates, daemon=True
        )
        self.listener_thread.start()
        self.update_handlers = []

    def connect(self):
        print("Connecting to server...")
        self.sock.connect((self.host, self.port))
        print("Connected to server")

    def reconnect(self):
        print("Reconnecting to server...")
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def send_request_and_get_response(self, path, method="POST", body=None):
        request_id = str(uuid.uuid4())
        response_queue = Queue()
        self.response_queues[request_id] = response_queue

        with self.lock:
            if body is None:
                body = {}
            body["request_id"] = request_id
            body_str = json.dumps(body)
            body_length = len(body_str.encode("utf-8"))
            request_line = f"{method} {path} HTTP/1.1\r\n"
            headers = f"Content-Length: {body_length}\r\n"
            request = f"{request_line}{headers}\r\n{body_str}"
            print(f"Sending request: {request}")
            self.sock.sendall(request.encode("utf-8"))

        response = response_queue.get(
            timeout=35
        )  # Wait for up to 10 seconds for a response
        del self.response_queues[request_id]
        return response

    def listen_for_updates(self):
        while True:
            try:
                data_chunk = self.sock.recv(8192).decode("utf-8")
                if data_chunk:
                    print("Received data chunk: " + data_chunk)

                    # Split the response into headers and body
                    header_part, body_part = data_chunk.split("\r\n\r\n", 1)
                    if "200" not in header_part:
                        raise Exception("Non-200 response")
                    body = json.loads(body_part)

                    self.handle_data(body)
            except socket.error:
                print("Socket error in listener thread, reconnecting...")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")

    def handle_data(self, data):
        request_id = data.get("request_id")
        if request_id and request_id in self.response_queues:
            self.response_queues[request_id].put(data.get("data"))
        else:
            self.handle_update(data.get("data"))

    def handle_update(self, data):
        for handler in self.update_handlers:
            handler(data)

    def add_update_handler(self, handler):
        self.update_handlers.append(handler)
