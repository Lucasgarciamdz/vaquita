from textual import on
from textual.screen import Screen
from textual.widgets import Button, Input, Static

from services.checking_account_svc import CheckingAccountSvc
from services.user_svc import UserSvc

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


class CreateVaquitaScreen(Screen):

    def __init__(self, user_id):
        super().__init__(
        )
        self.user_id = user_id

    @on(Button.Pressed, "#create_vaquita")
    def create_vaquita(self):
        form_data = self.query(Input)
        bank_name = form_data[0].value
        bank_balance = form_data[1].value
        password = form_data[2].value

        user_service.create_personal_bank(
            bank_name, bank_balance, self.user_id, password, personal=False
        )
        self.dismiss(True)

    def compose(self):
        yield Input(placeholder="Bank Name", id="bank_name")
        yield Input(placeholder="Initial Balance", id="bank_balance")
        yield Input(placeholder="Password", id="password", password=True)
        yield Button("Create Vaquita", variant="primary", id="create_vaquita")


class JoinVaquitaScreen(Screen):

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @on(Button.Pressed, "#join_vaquita")
    def join_vaquita(self):
        form_data = self.query(Input)
        account_number = form_data[0].value
        password = form_data[1].value

        if user_service.join_vaquita(self.user_id, account_number, password):
            self.dismiss(True)
        else:
            self.mount(Static("Error joining vaquita"))

    def compose(self):
        yield Input(placeholder="Account number", id="account_number")
        yield Input(placeholder="Password", id="password", password=True)
        yield Button("Join Vaquita", variant="primary", id="join_vaquita")

class ConfigCheckingAccountScreen(Screen):
    CSS_PATH = "./css/config_checking_account.css"

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
