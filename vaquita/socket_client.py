import json
import socket
import threading


class SocketClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SocketClient, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, host='localhost', port=22229):
        if self._initialized:
            return
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.lock = threading.Lock()
        self._initialized = True

    def connect(self):
        print("Connecting to server...")
        self.sock.connect((self.host, self.port))
        print("Connected to server")

    def reconnect(self):
        print("Reconnecting to server...")
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def send_request_and_get_response(self, path, method='POST', body=None):
        with self.lock:
            if body is None:
                body = {}
            body_str = json.dumps(body)
            body_length = len(body_str.encode('utf-8'))
            request_line = f"{method} {path} HTTP/1.1\r\n"
            headers = f"Content-Length: {body_length}\r\n"
            request = f"{request_line}{headers}\r\n{body_str}"
            print(f"Sending request: {request}")
            try:
                self.sock.sendall(request.encode('utf-8'))
                return self.receive_response()
            except socket.error:
                print("Socket error, reconnecting...")
                self.reconnect()
                self.sock.sendall(request.encode('utf-8'))
                return self.receive_response()

    def receive_response(self):
        data_chunk = self.sock.recv(8192).decode('utf-8')
        print("Received data chunk from the server: " + data_chunk)
        if not data_chunk:
            print("No data received from the server")
            return None
        else:
            lines = data_chunk.split('\r\n')
            status_line = lines[0]
            status_code = status_line.split(' ')[1]
            print(f"Received response: {status_line}")

            if "200" not in status_code:
                print("Error response received" + status_line)
                raise Exception("Error response received")

            headers = {}
            body_start_index = 0
            for i, line in enumerate(lines[1:], start=1):
                if line == '':
                    body_start_index = i + 1
                    break
                key, value = line.split(': ', 1)
                headers[key] = value

            content_length = int(headers.get('Content-Length', 0))
            body = '\r\n'.join(lines[body_start_index:])
            if len(body) < content_length:
                body = body.lstrip('\r\n')
            while len(body) < content_length:
                more_body = self.sock.recv(content_length - len(body)).decode('utf-8')
                body += more_body

            print(f"Body: {body}")
            return json.loads(body) if body else None

