from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Static, Tab, Tabs, Select
from textual.containers import ScrollableContainer


from enum import Enum as PyEnum
from socket_client import SocketClient
from terminal_ui.config_checking_account import ConfigCheckingAccountScreen


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
    def __init__(self, checking_account_list: list, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.checking_account_list = checking_account_list
        self.respose_dict = None

    def on_mount(self) -> None:
        if not self.query_one(Tabs).has_focus:
            self.query_one(Tabs).focus()

    def compose(self):
        tab_list = []
        if self.checking_account_list:
            for account in self.checking_account_list:
                tab = Tab(label=account["name"], id="id" + str(account["id"]))
                tab_list.append(tab)
        else:
            tab_list.append(Tab("No accounts found"))

        yield Tabs(*tab_list)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        return


class CheckingAccountTransactions(Widget):
    transactions_list = reactive("transactions_list", recompose=True)

    def __init__(self, transaction_list_initial):
        super().__init__()
        self.transactions_list = transaction_list_initial

    def render(self):
        header = "\nTransactions:\n" + "-" * 80 + "\n"
        header += (
            f"{'Date':<20}{'Type':<10}{'Category':<15}{'Amount':<10}{'Description':<25}\n"
            + "-" * 80
        )

        body = ""
        for transaction in self.transactions_list:
            date = transaction["date"]
            transaction_type = transaction["transaction_type"].capitalize()
            category = transaction["category"].capitalize()
            amount = f"${transaction['amount']:.2f}"
            description = transaction["description"][
                :25
            ]  # Truncate description if too long
            body += f"\n{date:<20}{transaction_type:<10}{category:<15}{amount:<10}{description:<25}"

        footer = "\n" + "-" * 80

        return header + body + footer


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
        notes = ""
        description = form_data[1].value

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
            "/checking_accounts/transactions/add", method="POST", body=body
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
        yield Input(placeholder="Description", id="description")
        yield Button("Add transaction", id="add_transaction")


class CheckingAccountScreen(Screen):
    CSS_PATH = "./css/account.tcss"

    refresh_transactions = reactive("refresh", recompose=True)

    def __init__(self, response_dict=None, user_id=None, account_id=None):
        super().__init__()
        self.user_id = user_id
        self.user_checking_accounts = None
        if not response_dict:
            if self.user_checking_accounts is None:
                self.user_checking_accounts = (
                    socket_client.send_request_and_get_response(
                        f"/users/accounts/{self.user_id}", method="GET"
                    )
                )

        else:
            self.user_checking_accounts = response_dict

        if account_id:
            self.current_account = next(
                account
                for account in self.user_checking_accounts
                if account["id"] == account_id
            )
            self.transactions_list = socket_client.send_request_and_get_response(
                f"/checking_accounts/transactions/{account_id}",
                method="GET",
            )
        else:
            self.transactions_list = self.user_checking_accounts[0]["transactions"]
            self.current_account = (
                self.user_checking_accounts[0] if account_id is None else account_id
            )
        socket_client.add_update_handler(self.handle_update)

    def handle_update(self, data):
        if data.get("type") == "transaction_update":
            self.transactions_list.append(data["transaction"])
            self.refresh_transactions = not self.refresh_transactions

    @on(Button.Pressed, "#add_transaction")
    def add_transaction(self):
        def reload_transactions(transaction_created):
            response = socket_client.send_request_and_get_response(
                f'/checking_accounts/transactions/{self.current_account["id"]}',
                method="GET",
            )
            self.transactions_list = response
            self.refresh_transactions = not self.refresh_transactions

        self.app.push_screen(
            AddTransactionScreen(self.user_id, self.current_account["id"]),
            callback=reload_transactions,
        )

    @on(Button.Pressed, "#add_checking_account")
    def on_add_checking_account_pressed(self):
        self.app.push_screen(
            ConfigCheckingAccountScreen(self.user_id),
            callback=CheckingAccountScreen(user_id=self.user_id),
        )

    @on(Tabs.TabActivated, "#id*")
    def on_tab_activated(self, event: Tabs.TabActivated):
        self.transactions_list = socket_client.send_request_and_get_response(
            f"/checking_accounts/transactions/{int(event.tab.id[2:])}",
            method="GET",
        )
        self.refresh_transactions = not self.refresh_transactions

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            CheckingAccountTabs(self.user_checking_accounts, self.user_id),
            Button("+", variant="success", id="add_checking_account"),
            Static("Account number: " + str(self.current_account["account_number"])),
            Static("Balance: " + str(self.current_account["balance"])),
            CheckingAccountTransactions(self.transactions_list),
            Button("Add transaction", id="add_transaction"),
        )
