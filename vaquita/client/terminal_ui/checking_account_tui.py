from enum import Enum as PyEnum

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from socket_client import SocketClient
from terminal_ui.config_checking_account import ConfigCheckingAccountScreen
from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Select, Static, Tab, Tabs

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


class AccountDetailsWidget(Widget):
    """Widget to display account details and transactions."""

    account_number = reactive("")
    balance = reactive(0.0)
    transactions = reactive([])

    def compose(self):
        yield Vertical(
            Static("", id="account_number"),
            Static("", id="balance"),
            Static("", id="transactions"),
        )

    def on_mount(self):
        self.update_display()

    def watch_account_number(self, new_value):
        self.update_display()

    def watch_balance(self, new_value):
        self.update_display()

    def watch_transactions(self, new_value):
        self.update_display()

    def update_display(self):
        self.query_one("#account_number", Static).update(
            f"Account number: {self.account_number}"
        )

        balance_text = f"Balance: ${self.balance:.2f}"
        balance_color = "green" if self.balance >= 0 else "red"
        self.query_one("#balance", Static).update(
            Text(balance_text, style=balance_color)
        )

        table = Table(title="Transactions", expand=True)
        table.add_column("Date", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Category", style="white")
        table.add_column("Amount", justify="right", style="cyan")
        table.add_column("Description")

        for transaction in self.transactions:
            date = transaction["date"]
            transaction_type = transaction["transaction_type"].capitalize()
            category = transaction["category"].capitalize()
            amount = transaction["amount"]
            sign = "+" if transaction_type == "Income" else "-"
            color = {"Income": "green", "Expense": "red", "Transfer": "blue"}.get(
                transaction_type, "white"
            )

            amount_str = f"{sign}${abs(amount):.2f}"
            description = transaction["description"][:25]

            table.add_row(
                date,
                Text(transaction_type, style=color),
                category,
                Text(amount_str, style=color),
                description,
            )

        panel = Panel(table, title="Transactions", border_style="blue")
        self.query_one("#transactions", Static).update(panel)


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
        self.calculate_balance()
        socket_client.add_update_handler(self.handle_update)

    def calculate_balance(self):
        balance = self.current_account["balance"]
        for transaction in self.transactions_list:
            if transaction["transaction_type"] == "INCOME":
                balance += transaction["amount"]
            else:
                balance -= transaction["amount"]
        self.current_account["balance"] = balance

    def handle_update(self, data):
        if data.get("type") == "transaction_update":
            self.transactions_list.append(data["transaction"])
            self.calculate_balance()
            self.update_account_details()

    def update_account_details(self):
        account_details = self.query_one(AccountDetailsWidget)
        account_details.account_number = str(self.current_account["account_number"])
        account_details.balance = self.current_account["balance"]
        account_details.transactions = self.transactions_list
        self.refresh()

    @on(Button.Pressed, "#add_transaction")
    def add_transaction(self):
        def reload_transactions(transaction_created):
            response = socket_client.send_request_and_get_response(
                f'/checking_accounts/transactions/{self.current_account["id"]}',
                method="GET",
            )
            self.transactions_list = response
            self.calculate_balance()
            self.update_account_details()

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

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            CheckingAccountTabs(self.user_checking_accounts, self.user_id),
            Button("New account +", variant="success", id="add_checking_account"),
            AccountDetailsWidget(),
            Button("Add transaction", id="add_transaction"),
        )

    def on_mount(self) -> None:
        self.update_account_details()
