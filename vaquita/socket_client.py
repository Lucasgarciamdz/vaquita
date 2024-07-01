# socket_client.py
import json
import socket
import threading
import uuid
from queue import Queue, Empty
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SocketClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.host = "localhost"
        self.port = 22229
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.lock = threading.Lock()
        self.response_queues = {}
        self.listener_thread = threading.Thread(
            target=self.listen_for_updates, daemon=True
        )
        self.listener_thread.start()
        self.update_handlers = []

    def connect(self):
        self.sock.connect((self.host, self.port))
        logging.info(f"Connected to server at {self.host}:{self.port}")

    def send_request_and_get_response(self, path, method="POST", body=None):
        request_id = str(uuid.uuid4())
        response_queue = Queue()
        self.response_queues[request_id] = response_queue

        if body is None:
            body = {}
        body["request_id"] = request_id
        body_str = json.dumps(body)
        request = f"{method} {path} HTTP/1.1\r\nContent-Length: {len(body_str)}\r\n\r\n{body_str}"

        with self.lock:
            self.sock.sendall(request.encode("utf-8"))
            logging.debug(f"Sent request: {request}")

        try:
            response = response_queue.get(timeout=20)  # Increase timeout to 20 seconds
        except Empty:
            logging.error("Request timed out")
            return None
        finally:
            del self.response_queues[request_id]

        return response

    def listen_for_updates(self):
        while True:
            try:
                data_chunk = self.sock.recv(8192).decode("utf-8")
                if data_chunk:
                    logging.debug(f"Received data chunk: {data_chunk}")
                    header_part, body_part = data_chunk.split("\r\n\r\n", 1)
                    if "200" not in header_part:
                        raise Exception("Non-200 response")
                    body = json.loads(body_part)
                    self.handle_data(body)
            except Exception as e:
                logging.error(f"Error in listener thread: {e}")

    def handle_data(self, data):
        logging.debug(f"Handling data: {data}")
        request_id = data.get("request_id")
        if request_id and request_id in self.response_queues:
            self.response_queues[request_id].put(data.get("data"))
        else:
            self.handle_update(data.get("data"))

    def handle_update(self, data):
        logging.debug(f"Handling update: {data}")
        for handler in self.update_handlers:
            handler(data)

    def add_update_handler(self, handler):
        self.update_handlers.append(handler)
