from textual.app import App
from textual.widgets import Button, ScrollView, Box
from textual import events
from bank_svc import BankSvc

class BankApp(App):
    bank_service = BankSvc()  # Aquí deberías pasar tu repositorio de cuentas

    async def on_mount(self):
        buttons = ScrollView()
        for command in ["create_bank", "join_bank", "create_account", "join_account", "quit"]:
            button = Button(command, name=command)
            buttons.add(button)
        await self.view.dock(buttons, edge="left", size=30)

    async def on_click(self, event: events.Click):
        if event.sender.name == 'quit':
            await self.quit()
        elif event.sender.name in ['join_bank', 'join_account']:
            code_or_name = await self.ask("Enter bank code or account name")
            if event.sender.name == 'join_bank':
                self.join_bank(code_or_name)
            else:
                self.join_account(code_or_name)
        elif event.sender.name == 'create_bank':
            self.create_bank()
        elif event.sender.name == 'create_account':
            self.create_account()

    def create_bank(self):
        bank_code = self.bank_service.create_bank()
        self.console.print(f"[green]Created new bank with code {bank_code}[/green]")

    def join_bank(self, bank_code: str):
        self.bank_service.join_bank(bank_code)
        self.console.print(f"[blue]Joined bank with code {bank_code}[/blue]")

    def create_account(self):
        account_name = self.bank_service.create_account()
        self.console.print(f"[magenta]Created new account with name {account_name}[/magenta]")

    def join_account(self, account_name: str):
        self.bank_service.join_account(account_name)
        self.console.print(f"[cyan]Joined account with name {account_name}[/cyan]")

BankApp.run()