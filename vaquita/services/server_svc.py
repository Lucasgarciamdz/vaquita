import socket
import threading

class ServerSvc:
    def __init__(self, host='::', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def handle_client(self, client_socket, client_address):
        while True:
            # Recibir el comando del cliente
            command = client_socket.recv(1024).decode()

            # Si el cliente envía el comando 'quit', terminar la conexión
            if command.lower() == 'quit':
                break

            # Aquí es donde manejarías los otros comandos
            # Por ejemplo, podrías tener comandos para depositar, retirar, etc.
            # Para cada comando, realizarías la operación correspondiente en la cuenta del usuario
            # y luego enviarías una respuesta al cliente

            # Por ejemplo, aquí hay un esqueleto de cómo podrías manejar un comando de depósito:
            if command.startswith('deposit'):
                _, account_name, amount = command.split()
                amount = int(amount)

                # Aquí es donde depositarías el monto en la cuenta
                # Por ejemplo, podrías hacer algo como esto:
                # self.account_repository.get_account(account_name).deposit(amount)

                # Luego enviarías una respuesta al cliente para confirmar que el depósito fue exitoso
                response = f'Deposited {amount} into {account_name}'
                client_socket.sendall(response.encode())

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()