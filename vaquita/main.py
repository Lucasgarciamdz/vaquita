from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from database.database_manager import DatabaseManager
from terminal_ui.checking_account_tui import AccountScreen
from terminal_ui.user_tui import RegisterForm, LoginForm
from terminal_ui.welcoming_tui import WelcomingScreen

db = DatabaseManager()


class VaquitaApp(App):
    """
    VaquitaApp is a textual app that displays a custom welcome message when started.
    """

    def on_mount(self):
        def check_form(form):
            if form == 'register':
                self.push_screen(screen=RegisterForm())
            elif form == 'login':
                self.push_screen(screen=LoginForm())

        self.push_screen(WelcomingScreen(), check_form)
        db.create_database()

    def compose(self) -> ComposeResult:
        yield Header()
        self.push_screen(AccountScreen())
        yield Footer()


app = VaquitaApp()
app.run()
