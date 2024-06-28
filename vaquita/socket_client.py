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
        self.host = host  # Set the host attribute
        self.port = port  # Set the port attribute
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.lock = threading.Lock()
        self._initialized = True

    def ensure_connection(self):
        try:
            # Attempt to send a zero-length packet as a connection check.
            self.sock.sendall(b'')
        except socket.error:
            # If sending fails, re-establish the connection.
            self.sock.connect((self.host, self.port))

    def send_request_and_get_response(self, path, method='POST', body=None):
        with self.lock:
            self.ensure_connection()
            if body is None:
                body = {}
            body_str = json.dumps(body)
            body_length = len(body_str.encode('utf-8'))
            request_line = f"{method} {path} HTTP/1.1\r\n"
            headers = f"Content-Length: {body_length}\r\n"
            request = f"{request_line}{headers}\r\n{body_str}"
            self.sock.sendall(request.encode('utf-8'))

            return self.receive_response()

    def receive_response(self):
        print("Receiving response")
        # Initial large chunk receive
        data_chunk = self.sock.recv(4096).decode('utf-8')
        if data_chunk == '':
            return None
        else:
            # Splitting the chunk into lines
            lines = data_chunk.split('\r\n')

            # Extracting status code from the status line
            status_line = lines[0]
            status_code = status_line.split(' ')[1]

            # Parsing headers
            headers = {}
            body_start_index = 0
            for i, line in enumerate(lines[1:], start=1):  # Start from the second line
                if line == '':  # Empty line indicates end of headers
                    body_start_index = i + 1
                    break
                key, value = line.split(': ', 1)
                headers[key] = value

            # Determining how much of the body has been received and how much more needs to be read
            content_length = int(headers.get('Content-Length', 0))
            body = '\r\n'.join(lines[body_start_index:])  # Initial body part
            while len(body) < content_length:
                more_body = self.sock.recv(content_length - len(body)).decode('utf-8')
                body += more_body

            print(f"Received response: {status_line}")
            print(f"STATUS: {status_code}")
            print(f"HEADERS: {headers}")
            print(f"BODY: {body}")

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
    response = client.send_request_and_get_response('/users/login', 'POST', {'email': 'example@example.com', 'password': 'password'})
    print(f"Response: {response}")
    client.close()
