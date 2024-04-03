from textual import events, on
from textual.app import App
from textual.screen import Screen
from textual.widgets import Button, Input, Static
from services.checking_account_svc import CheckingAccountSvc

account_service = CheckingAccountSvc()

class ConfigCheckingAccountScreen(Screen):
    CSS_PATH = "./css/config_checking_account.css"

    def __init__(self, user_id):
        self.user_id = user_id

    @on(Button.Pressed, "#create_bank")
    def show_create_bank(self):
        self.dismiss("create_bank")

    @on(Button.Pressed, "#join_vaquita")
    def show_join_vaquita(self):
        vaquita_number = self.query_one(Input).value

        account_service.join_account(vaquita_number, self.user_id)
        self.dismiss("join_vaquita")

    def compose(self):
        yield Static("Welcome to Vaquita! Please create a bank or join an existing one." + self.user_id)
        yield Button("Create Bank", variant="primary", id="create_bank")
        yield Input(placeholder="Vaquita number", id="vaquita_number")
        yield Button("Join Vaquita", variant="primary", id="join_vaquita")