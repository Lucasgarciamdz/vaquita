import json

from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Static


from http.client import HTTPConnection
from socket_client import SocketClient


class RegisterForm(Screen):
    CSS_PATH = "./css/user.css"

    def __init__(self):
        super().__init__()
        self.socket_client = SocketClient()

    @on(Button.Pressed, "#register_btn")
    def return_to_main(self):
        form_data = self.query(Input)
        name = form_data[0].value
        email = form_data[1].value
        password = form_data[2].value

        try:
            response_dict = self.socket_client.send_request_and_get_response('/users/register', 'POST', {'name': name, 'email': email, 'password': password})
            if response_dict:
                user_id = response_dict['user_id']
                self.dismiss(user_id)
            else:
                raise Exception('No response received from the server')
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Name")
        yield Input(placeholder="Email")
        yield Input(password=True, placeholder="Password")
        yield Button("Register", id="register_btn")


class LoginForm(Screen):
    CSS_PATH = "./css/user.css"

    def __init__(self):
        super().__init__()
        self.socket_client = SocketClient()

    @on(Button.Pressed, "#login_btn")
    def return_to_main(self):
        form_data = self.query(Input)
        email = form_data[0].value
        password = form_data[1].value

        try:
            response_dict = self.socket_client.send_request_and_get_response('/users/login', 'POST', {'email': email, 'password': password})
            if response_dict:
                user_id = response_dict['user_id']
                if isinstance(user_id, int):
                    self.dismiss(user_id)
                elif user_id == "false":
                    raise Exception('Incorrect user')
                else:
                    raise Exception('Unexpected user_id value received from the server')
            else:
                raise Exception('No response received from the server')
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Email")
        yield Input(password=True, placeholder="Password")
        yield Button("Login", id="login_btn")
