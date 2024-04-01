from textual.app import App
from textual.widgets import Button, ScrollView
from textual import events
from checking_account_svc import CheckingAccountSvc
from vaquita.config.logger_config import setup_custom_logger

LOG = setup_custom_logger(__name__)

class BankApp(App):
    account_service = CheckingAccountSvc()  # Aquí deberías pasar tu repositorio de cuentas

    async def on_mount(self):
        buttons = ScrollView()
        for command in ["deposit", "withdraw", "balance", "add_transaction", "list_transactions", "quit"]:
            button = Button(command, name=command)
            buttons.add(button)
        await self.view.dock(buttons, edge="left", size=30)
        LOG.debug("Mounted buttons on view")

    async def on_click(self, event: events.Click):
        LOG.info(f"Button clicked: {event.sender.name}")
        if event.sender.name == 'quit':
            await self.quit()
        else:
            account_name = await self.ask("Enter account name")
            if event.sender.name in ['deposit', 'withdraw']:
                amount = await self.ask("Enter amount", converter=int)
                if event.sender.name == 'deposit':
                    self.deposit(account_name, amount)
                else:
                    self.withdraw(account_name, amount)
            elif event.sender.name == 'balance':
                self.balance(account_name)
            elif event.sender.name == 'add_transaction':
                transaction = await self.ask("Enter transaction")
                self.add_transaction(account_name, transaction)
            elif event.sender.name == 'list_transactions':
                self.list_transactions(account_name)

    def deposit(self, account_name: str, amount: int):
        self.account_service.deposit(account_name, amount)
        self.console.print(f"[green]Deposited {amount} into {account_name}[/green]")
        LOG.info(f"Deposited {amount} into {account_name}")

    def withdraw(self, account_name: str, amount: int):
        self.account_service.withdraw(account_name, amount)
        self.console.print(f"[red]Withdrew {amount} from {account_name}[/red]")
        LOG.info(f"Withdrew {amount} from {account_name}")

    def balance(self, account_name: str):
        balance = self.account_service.get_balance(account_name)
        self.console.print(f"[blue]Balance for {account_name}: {balance}[/blue]")
        LOG.info(f"Balance for {account_name}: {balance}")

    def add_transaction(self, account_name: str, transaction: str):
        self.account_service.add_transaction(account_name, transaction)
        self.console.print(f"[magenta]Added transaction: {transaction}[/magenta]")
        LOG.info(f"Added transaction: {transaction}")

    def list_transactions(self, account_name: str):
        transactions = self.account_service.get_transactions(account_name)
        for transaction in transactions:
            self.console.print(f"[cyan]{transaction}[/cyan]")
            LOG.info(f"Transaction: {transaction}")

BankApp.run()