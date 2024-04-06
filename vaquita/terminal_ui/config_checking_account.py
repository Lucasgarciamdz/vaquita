from services.checking_account_svc import CheckingAccountSvc
from services.user_svc import UserSvc
from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Static

account_service = CheckingAccountSvc()
user_service = UserSvc()


class CreateBankScreen(Screen):

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @on(Button.Pressed, "#create_bank")
    def create_bank(self):
        form_data = self.query(Input)
        bank_name = form_data[0].value
        bank_balance = form_data[1].value

        user_service.create_personal_bank(
            bank_name, bank_balance, self.user_id, "password", personal=True
        )
        self.dismiss(True)

    def compose(self):
        yield Input(placeholder="Bank Name", id="bank_name")
        yield Input(placeholder="Initial Balance", id="bank_balance")
        yield Button("Create Personal Bank", variant="primary", id="create_bank")


class ConfigCheckingAccountScreen(Screen):
    CSS_PATH = "./css/config_checking_account.css"

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @on(Button.Pressed, "#create_bank")
    def show_create_bank(self):

        def check_bank_created(created):
            if created:
                self.app.pop_screen()
            else:
                self.mount(Static("Error creating bank"))

        self.app.push_screen(CreateBankScreen(self.user_id), check_bank_created)

    @on(Button.Pressed, "#join_vaquita")
    def show_join_vaquita(self):
        vaquita_number = self.query_one(Input).value

        account_service.join_account(vaquita_number, self.user_id)
        self.dismiss("join_vaquita")

    def compose(self):
        yield Static(
            "Welcome to Vaquita! Please create a bank or join an existing one. user id: "
            + str(self.user_id)
        )
        yield Button("Create personal Bank", variant="primary", id="create_bank")
        yield Button("Create Vaquita", variant="primary", id="create_vaquita")
        yield Button("Join Vaquita", variant="primary", id="join_vaquita")
