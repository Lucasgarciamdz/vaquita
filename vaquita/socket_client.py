import socket
import json
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.lock = threading.Lock()
        self._initialized = True

    def send_request_and_get_response(self, path, method='GET', body=None):
        with self.lock:
            if body is None:
                body = {}
            body_str = json.dumps(body)
            request_line = f"{method} {path} HTTP/1.1\r\n"
            headers = f"Content-Length: {len(body_str.encode('utf-8'))}\r\n"
            request = f"{request_line}{headers}\r\n{body_str}"
            print(f"Sending request:\n{request}")  # Debug statement
            self.sock.sendall(request.encode('utf-8'))

            return self.receive_response()

    def receive_response(self):
        response_line = self.sock.recv(4096).decode('utf-8').strip()
        headers = {}
        while True:
            line = self.sock.recv(4096).decode('utf-8').strip()
            if line == '':
                break
            key, value = line.split(': ', 1)
            headers[key] = value

        content_length = int(headers.get('Content-Length', 0))
        body = self.sock.recv(content_length).decode('utf-8')

        return json.loads(body) if body else None

    def close(self):
        with self.lock:
            self.sock.close()
            self._initialized = False

    def receive_forever(self):
        while True:
            data = self.receive_response()
            if data:
                print(f"Received data: {data}")


# Usage example
if __name__ == "__main__":
    client = SocketClient()
    response = client.send_request_and_get_response('/readyz', 'GET')
    print(f"Response: {response}")
    client.close()
