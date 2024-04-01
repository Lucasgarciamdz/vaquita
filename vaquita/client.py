import socket
from textual.app import App
from textual.widgets import Button, ScrollView
from textual import events
from vaquita.terminal_ui.user_tui import UserApp
from vaquita.config.logger_config import setup_custom_logger
from vaquita.terminal_ui.bank_tui import BankApp

LOG = setup_custom_logger(__name__)

class ClientApp(App):
    def __init__(self, host='localhost', port=12345):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        LOG.info(f"Connected to server at {host}:{port}")

    async def on_mount(self):
        buttons = ScrollView()
        for command in ["personal account", "vaquita", "quit"]:
            button = Button(command, name=command)
            buttons.add(button)
        await self.view.dock(buttons, edge="left", size=30)
        LOG.debug("Mounted buttons on view")

    async def on_click(self, event: events.Click):
        LOG.info(f"Button clicked: {event.sender.name}")
        if event.sender.name == 'quit':
            self.client_socket.sendall('quit'.encode())
            LOG.debug("Sent 'quit' command to server")
            await self.quit()
        elif event.sender.name == 'personal account':
            user_app = UserApp()
            await user_app.run()
            LOG.debug("Ran UserApp")
        elif event.sender.name == 'vaquita':
            bank_app = BankApp()
            await bank_app.run()
            LOG.debug("Ran BankApp")
        else:
            self.client_socket.sendall(event.sender.name.encode())
            LOG.debug(f"Sent '{event.sender.name}' command to server")
            response = self.client_socket.recv(1024).decode()
            self.console.print(response)
            LOG.info(f"Received response from server: {response}")

    async def on_exit(self, event: events.Exit):
        self.client_socket.close()
        LOG.info("Closed connection to server")

ClientApp.run()