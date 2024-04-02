from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input


class RegisterForm(Screen):

    CSS_PATH = "./css/user.css"

    @on(Button.Pressed, "#register_btn")
    def return_to_main(self):
        self.dismiss(True)

    def compose(self):
        yield Input(placeholder="Name")
        yield Input(placeholder="Email")
        yield Input(placeholder="Password")
        yield Button("Register", id="register_btn")


class LoginForm(Screen):
    CSS_PATH = "./css/user.css"


    @on(Button.Pressed, "#login_btn")
    def return_to_main(self):
        self.dismiss(True)

    def compose(self):
        yield Input(placeholder="Email")
        yield Input(placeholder="Password")
        yield Button("Login", id="login_btn")
