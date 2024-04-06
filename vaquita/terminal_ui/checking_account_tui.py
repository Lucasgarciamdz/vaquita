from services.user_svc import UserSvc
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Static, Tab, Tabs

user_svc = UserSvc()


class CheckingAcoountTabs(Widget):

    def __init__(self, checking_account_list: list):
        super().__init__()
        self.checking_account_list = checking_account_list

    def compose(self):

        tabs = Tabs()
        if self.checking_account_list:
            for account in self.checking_account_list:
                tab = Tab(label=account.name, id=account.id)
                tabs.add_tab(tab)
        else:
            tabs.add_tab(Static("No accounts found"))

        yield tabs


class CheckingAccountTransactions(Widget):

    def __init__(self, transaction_list: list):
        super().__init__()
        self.transactions = transaction_list

    def compose(self):
        if self.transactions:
            for transaction in self.transactions:
                yield Static(transaction['date'] + " " + transaction['description'] + " " + transaction['amount'])
        else:
            yield Static("No transactions found")


class AddTransactionScreen(Screen):

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    def on_mount(self, user_id):
        self.user_id = user_id

    @on(Button.Pressed, "Submit")
    def add_transaction(self, event):
        form_data = self.query(Input)
        amount = form_data[0].value
        description = form_data[1].value
        user_svc.add_transaction(self.user_id, amount, description)
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Label("Add transaction")
        yield Input("Amount", id="Amount")
        yield Input("Description", id="Description")
        yield Button("Submit", id="Submit")


class CheckingAccountScreen(Screen):

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    def on_mount(self, user_id):
        self.user_id = user_id
        self.user_checking_accounts = user_svc.get_user_accounts(self.user_id)
        self.transactions_list = self.user_checking_accounts[0].get_transactions()

    @on(Button.Pressed, "Add_transaction")
    def add_transaction(self, event):
        self.app.push_screen(AddTransactionScreen(self.user_id))

    def compose(self) -> ComposeResult:
        yield CheckingAcoountTabs(self.user_id)
        yield Static("Account number: " + str(self.user_checking_accounts[0].account_number))
        yield Static("Balance: " + str(user_svc.get_user_balance(self.user_id)))
        yield CheckingAccountTransactions(self.user_id)
        yield Button("Add transaction", id="Add_transaction")
