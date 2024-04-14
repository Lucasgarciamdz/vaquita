from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Static

import requests

class RegisterForm(Screen):
    CSS_PATH = "./css/user.css"

    @on(Button.Pressed, "#register_btn")
    def return_to_main(self):
        form_data = self.query(Input)
        name = form_data[0].value
        email = form_data[1].value
        password = form_data[2].value

        try:
            response = requests.post('http://localhost:8000/users/register', json={'name': name, 'email': email, 'password': password})
            response.raise_for_status()
            user_id = response.json()['user_id']
            self.dismiss(user_id)
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Name")
        yield Input(placeholder="Email")
        yield Input(password=True, placeholder="Password")
        yield Button("Register", id="register_btn")

class LoginForm(Screen):
    CSS_PATH = "./css/user.css"

    @on(Button.Pressed, "#login_btn")
    def return_to_main(self):
        form_data = self.query(Input)
        email = form_data[0].value
        password = form_data[1].value

        try:
            response = requests.post('http://localhost:8000/users/login', json={'email': email, 'password': password})
            response.raise_for_status()
            user_id = response.json()['user_id']
            self.dismiss(user_id)
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Email")
        yield Input(password=True, placeholder="Password")
        yield Button("Login", id="login_btn")