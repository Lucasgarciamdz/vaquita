from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

from database.database_manager import DatabaseManager
from services.checking_account_svc import CheckingAccountSvc
from services.user_svc import UserSvc
from terminal_ui.config_checking_account import ConfigCheckingAccountScreen
from terminal_ui.user_tui import RegisterForm, LoginForm
from terminal_ui.welcoming_tui import WelcomingScreen

db = DatabaseManager()

checking_account_service = CheckingAccountSvc()

user_service = UserSvc()


class VaquitaApp(App):
    """
    VaquitaApp is a textual app that displays a custom welcome message when started.
    """

    user_id = None

    def on_mount(self):
        db.delete_database()
        db.create_database()

        def display_main_menu(user_id):
            self.push_screen(ConfigCheckingAccountScreen(user_id))
            # if user_service.get_user_accounts(user_id):
            # else:
            #     self.push_screen(AccountScreen(user_id))

        def check_form(form):
            if form == 'register':
                self.push_screen(screen=RegisterForm(), callback=display_main_menu)
            elif form == 'login':
                self.push_screen(screen=LoginForm(), callback=display_main_menu)

        self.push_screen(WelcomingScreen(), check_form)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to Vaquita!")

        yield Footer()


app = VaquitaApp()
app.run()
