from textual import on
from textual.screen import Screen
from textual.widgets import Button


class WelcomingScreen(Screen):
    CSS_PATH = "./css/user.css"

    @on(Button.Pressed, "#register")
    def show_register(self):
        self.dismiss("register")

    @on(Button.Pressed, "#login")
    def show_login(self):
        self.dismiss("login")

    def compose(self):
        yield Button("Register", variant="primary", id="register")
        yield Button("Login", variant="primary", id="login")
