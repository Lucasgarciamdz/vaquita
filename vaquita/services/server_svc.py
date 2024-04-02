import socketserver
import threading


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = str(self.request.recv(1024), 'utf-8')
            if data == 'create':
                response = 'Creating a wallet...'
                # Add your wallet creation logic here
            elif data == 'join':
                response = 'Joining a wallet...'
                # Add your wallet joining logic here
            else:
                response = 'Invalid option. Please send "create" or "join".'
            self.request.sendall(bytes(response, 'utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def start_server(host, port):
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f'Server started on {host}:{port}')


if __name__ == "__main__":
    import sys

    HOST, PORT = "localhost", int(sys.argv[1])
    start_server(HOST, PORT)
