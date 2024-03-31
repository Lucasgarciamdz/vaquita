import socket
from textual.app import App
from textual.widgets import Button, ScrollView
from textual import events
from vaquita.terminal_ui.user_tui import UserApp
from vaquita.terminal_ui.bank_tui import BankApp

class ClientApp(App):
    def __init__(self, host='localhost', port=12345):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    async def on_mount(self):
        buttons = ScrollView()
        for command in ["personal account", "vaquita", "quit"]:
            button = Button(command, name=command)
            buttons.add(button)
        await self.view.dock(buttons, edge="left", size=30)

    async def on_click(self, event: events.Click):
        if event.sender.name == 'quit':
            self.client_socket.sendall('quit'.encode())
            await self.quit()
        elif event.sender.name == 'personal account':
            user_app = UserApp()
            await user_app.run()
        elif event.sender.name == 'vaquita':
            bank_app = BankApp()
            await bank_app.run()
        else:
            self.client_socket.sendall(event.sender.name.encode())
            response = self.client_socket.recv(1024).decode()
            self.console.print(response)

    async def on_exit(self, event: events.Exit):
        self.client_socket.close()

ClientApp.run()