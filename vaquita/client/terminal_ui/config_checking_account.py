from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Static

from socket_client import SocketClient


class CreateBankScreen(Screen):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
        self.socket_client = SocketClient()

    @on(Button.Pressed, "#create_bank")
    def create_bank(self):
        form_data = self.query(Input)
        bank_name = form_data[0].value
        bank_balance = form_data[1].value

        try:
            response_dict = self.socket_client.send_request_and_get_response(
                "/users/create_personal_bank",
                "POST",
                {
                    "bank_name": bank_name,
                    "bank_balance": bank_balance,
                    "user_id": self.user_id,
                    "password": "password",
                    "personal": True,
                },
            )

            if response_dict:
                self.dismiss(True)
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Bank Name", id="bank_name")
        yield Input(placeholder="Initial Balance", id="bank_balance")
        yield Button("Create Personal Bank", variant="primary", id="create_bank")


class CreateVaquitaScreen(Screen):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.socket_client = SocketClient()

    @on(Button.Pressed, "#create_vaquita")
    def create_vaquita(self):
        form_data = self.query(Input)
        bank_name = form_data[0].value
        bank_balance = form_data[1].value
        password = form_data[2].value

        response_dict = self.socket_client.send_request_and_get_response(
            "/users/create_vaquita",
            "POST",
            {
                "bank_name": bank_name,
                "bank_balance": bank_balance,
                "user_id": self.user_id,
                "password": password,
                "personal": False,
            },
        )
        if response_dict:
            self.dismiss(True)
        else:
            raise Exception("No response received from the server")

    def compose(self):
        yield Input(placeholder="Bank Name", id="bank_name")
        yield Input(placeholder="Initial Balance", id="bank_balance")
        yield Input(placeholder="Password", id="password", password=True)
        yield Button("Create Vaquita", variant="primary", id="create_vaquita")


class JoinVaquitaScreen(Screen):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.socket_client = SocketClient()

    @on(Button.Pressed, "#join_vaquita")
    def join_vaquita(self):
        form_data = self.query(Input)
        account_number = form_data[0].value
        password = form_data[1].value

        try:
            response_dict = self.socket_client.send_request_and_get_response(
                "/users/join_vaquita",
                "POST",
                {
                    "user_id": self.user_id,
                    "vaquita_number": account_number,
                    "password": password,
                },
            )
            if response_dict and response_dict["result"]:
                self.dismiss(True)
            else:
                self.mount(Static("Error joining vaquita"))
        except Exception as e:
            self.mount(Static(str(e)))

    def compose(self):
        yield Input(placeholder="Account number", id="account_number")
        yield Input(placeholder="Password", id="password", password=True)
        yield Button("Join Vaquita", variant="primary", id="join_vaquita")


class ConfigCheckingAccountScreen(Screen):
    CSS_PATH = "css/config_checking_account.css"

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @on(Button.Pressed, "#create_bank")
    def show_create_bank(self):
        def check_bank_created(created):
            if created:
                self.dismiss(self.user_id)
            else:
                self.mount(Static("Error creating bank"))

        self.app.push_screen(CreateBankScreen(self.user_id), check_bank_created)

    @on(Button.Pressed, "#create_vaquita")
    def show_create_vaquita(self):
        def check_vaquita_created(created):
            if created:
                self.dismiss(self.user_id)
            else:
                self.mount(Static("Error creating vaquita"))

        self.app.push_screen(CreateVaquitaScreen(self.user_id), check_vaquita_created)

    @on(Button.Pressed, "#join_vaquita")
    def show_join_vaquita(self):
        def check_vaquita_joined(created):
            if created:
                self.dismiss(self.user_id)
            else:
                self.mount(Static("Error creating vaquita"))

        self.app.push_screen(JoinVaquitaScreen(self.user_id), check_vaquita_joined)

    def compose(self):
        yield Static(
            "Welcome to Vaquita! Please create a bank or join an existing one. user id: "
            + str(self.user_id)
        )
        yield Button("Create personal Bank", variant="primary", id="create_bank")
        yield Button("Create Vaquita", variant="primary", id="create_vaquita")
        yield Button("Join Vaquita", variant="primary", id="join_vaquita")
