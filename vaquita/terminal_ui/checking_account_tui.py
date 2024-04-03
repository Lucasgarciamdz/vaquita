from services.checking_account_svc import CheckingAccountSvc
from textual import on
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Input, Label

account_service = CheckingAccountSvc()


class TransactionList(ScrollableContainer):
    CSS_PATH = "./css/account.css"

    def compose(self):
        transactions = account_service.get_transactions("account_name")
        for transaction in transactions:
            yield Label(f"[cyan]{transaction}[/cyan]")


class AddTransactionForm(Screen):
    CSS_PATH = "./css/account.css"

    @on(Button.Pressed, "#add_transaction_btn")
    def add_transaction(self):
        form_data = self.query(Input)
        transaction = form_data[0]

        try:
            account_service.add_transaction("account_name", transaction)
            self.dismiss(True)
        except Exception as e:
            self.mount(Label(str(e)))

    def compose(self):
        yield Input(placeholder="Transaction")
        yield Button("Add Transaction", id="add_transaction_btn")


class AccountScreen(Screen):
    CSS_PATH = "./css/account.css"

    def __init__(self, user):
        self.user = user

    def compose(self):
        balance = account_service.get_balance("account_name")
        yield Label(f"[blue]Balance for account_name: {10}[/blue]")
        yield TransactionList()
        yield AddTransactionForm()
