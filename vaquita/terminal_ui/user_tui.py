from services.user_svc import UserSvc
from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static

user_svc = UserSvc()


class RegisterForm(Screen):
    CSS_PATH = "./css/user.css"

    @on(Button.Pressed, "#register_btn")
    def return_to_main(self):
        form_data = self.query(Input)
        name = form_data[0].value
        email = form_data[1].value
        password = form_data[2].value

        try:
            user_id = user_svc.register(name, email, password)
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
            user_id = user_svc.login(email, password)
            self.dismiss(user_id)
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Email")
        yield Input(password=True, placeholder="Password")
        yield Button("Login", id="login_btn")
