from textual.app import App
from textual.widgets import Button, ScrollView, Box
from textual import events

class UserApp(App):
    async def on_mount(self):
        buttons = ScrollView()
        for command in ["register", "login", "quit"]:
            button = Button(command, name=command)
            buttons.add(button)
        await self.view.dock(buttons, edge="left", size=30)

    async def on_click(self, event: events.Click):
        if event.sender.name == 'quit':
            await self.quit()
        elif event.sender.name == 'register':
            username = await self.ask("Enter username for registration")
            password = await self.ask("Enter password for registration", password=True)
            self.console.print(f"Registering user: {username}")
            # Here you would call your registration function with the username and password
        elif event.sender.name == 'login':
            username = await self.ask("Enter username for login")
            password = await self.ask("Enter password for login", password=True)
            self.console.print(f"Logging in user: {username}")
            # Here you would call your login function with the username and password

UserApp.run()