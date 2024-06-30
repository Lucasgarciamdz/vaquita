from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Static, Tab, Tabs, Select

from enum import Enum as PyEnum
from socket_client import SocketClient


socket_client = SocketClient()


class TransactionCategory(PyEnum):
    FOOD = "Food"
    RENT = "Rent"
    SERVICES = "Services"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"
    HEALTH = "Health"
    INSURANCE = "Insurance"
    PERSONAL = "Personal"
    ENTERTAINMENT = "Entertainment"
    EDUCATION = "Education"
    SAVINGS = "Savings"
    SALARY = "Salary"


class TransactionType(PyEnum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"


class CheckingAccountTabs(Widget):
    def __init__(self, checking_account_list: list):
        super().__init__()
        self.checking_account_list = checking_account_list

    def compose(self):
        tab_list = []
        if self.checking_account_list:
            for account in self.checking_account_list:
                tab = Tab(label=account["name"], id="id" + str(account["id"]))
                tab_list.append(tab)
        else:
            tab_list.append(Tab("No accounts found"))

        yield Tabs(*tab_list)


class CheckingAccountTransactions(Widget):
    transactions_list = reactive([], recompose=True)

    def __init__(self, transaction_list_initial):
        super().__init__()
        self.transactions_list_initial = transaction_list_initial

    def compose(self):
        for transaction in self.transactions_list_initial:
            yield Static(
                str(
                    str(transaction["date"])
                    + " "
                    + str(transaction["description"])
                    + " "
                    + str(transaction["amount"])
                )
            )


class AddTransactionScreen(Screen):
    def __init__(self, user_id: int, account_id: int):
        super().__init__()
        self.category = None
        self.user_id = user_id
        self.account_id = account_id
        self.transaction_types = [(t.name, t.name) for t in TransactionType]
        self.transaction_categories = [(c.name, c.name) for c in TransactionCategory]

        self.transaction_categorie = None
        self.transaction_type = None

    @on(Button.Pressed, "#add_transaction")
    def add_transaction(self, event):
        form_data = self.query(Input)
        amount = form_data[0].value
        notes = form_data[1].value
        description = form_data[2].value

        body = {
            "account_id": self.account_id,
            "amount": amount,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "notes": notes,
            "user_id": self.user_id,
            "description": description,
        }

        socket_client.send_request_and_get_response(
            "/transactions/add", method="POST", body=body
        )

        self.dismiss(True)

    @on(Select.Changed, "#transaction_types")
    def select_transaction_type(self, event):
        self.transaction_type = event.value

    @on(Select.Changed, "#transaction_categories")
    def select_transaction_category(self, event):
        self.category = event.value

    def compose(self) -> ComposeResult:
        yield Static("Add transaction")
        yield Input(placeholder="Amount", id="amount")
        yield Select(self.transaction_types, id="transaction_types")
        yield Select(self.transaction_categories, id="transaction_categories")
        yield Input(placeholder="Notes", id="notes")
        yield Input(placeholder="Description", id="description")
        yield Button("Add transaction", id="add_transaction")


class CheckingAccountScreen(Screen):
    refresh_transactions = reactive(False, recompose=True)

    def __init__(self, response_dict, user_id):
        super().__init__()
        self.user_id = user_id
        self.user_checking_accounts = response_dict
        self.transactions_list = self.user_checking_accounts[0]["transactions"]
        self.current_account = self.user_checking_accounts[0]
        socket_client.add_update_handler(self.handle_update)

    def handle_update(self, data):
        # Update logic based on received data
        if data.get("type") == "transaction_update":
            if data.get("account_id") == self.current_account["id"]:
                self.transactions_list.append(data["transaction"])
                self.refresh_transactions = not self.refresh_transactions

    @on(Button.Pressed, "#add_transaction")
    def add_transaction(self):
        def reload_transactions(transaction_created):
            response = socket_client.send_request_and_get_response(
                f'/accounts/{self.current_account["id"]}/transactions', method="GET"
            )
            self.transactions_list = response.get("transactions", [])
            self.refresh_transactions = not self.refresh_transactions

        self.app.push_screen(
            AddTransactionScreen(self.user_id, self.current_account["id"]),
            callback=reload_transactions,
        )

    def compose(self) -> ComposeResult:
        yield CheckingAccountTabs(self.user_checking_accounts)
        yield Static("Account number: " + str(self.current_account["account_number"]))
        yield Static("Balance: " + str(self.current_account["balance"]))
        yield CheckingAccountTransactions(self.transactions_list)
        yield Button("Add transaction", id="add_transaction")
