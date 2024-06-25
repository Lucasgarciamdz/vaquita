import http.client
import json

class HttpClient:
    def __init__(self, host='localhost', port=8080):
        self.conn = http.client.HTTPConnection(host, port)

    def send(self, path, method='GET', body=None, headers=None):
        if headers is None:
            headers = {}
        body_str = json.dumps(body) if body else ""
        headers['Content-Length'] = str(len(body_str.encode('utf-8')))
        try:
            self.conn.request(method, path, body_str, headers)
        except Exception as err:
            print(f'An error occurred: {err}')
            return None

    def receive(self):
        try:
            response = self.conn.getresponse()
            return response.status, response.read().decode()
        except Exception as err:
            print(f'An error occurred: {err}')
            return None

    def send_request_and_get_response(self, path, method='GET', body=None):
        self.send(path, method, body)
        response = self.receive()
        if response is not None:
            status, response_body = response
            if response_body is not None:
                return json.loads(response_body)
            else:
                raise Exception('No response received from the server')
        else:
            raise Exception('An error occurred while receiving the response', self.receive())

    def close(self):
        self.conn.close()