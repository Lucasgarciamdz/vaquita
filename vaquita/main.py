import json

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

from database.database_manager import DatabaseManager
from services.checking_account_svc import CheckingAccountSvc
from services.user_svc import UserSvc
from terminal_ui.checking_account_tui import CheckingAccountScreen
from terminal_ui.config_checking_account import ConfigCheckingAccountScreen
from terminal_ui.user_tui import RegisterForm, LoginForm
from terminal_ui.welcoming_tui import WelcomingScreen
import http.client
from http_client import HttpClient

db = DatabaseManager()

checking_account_service = CheckingAccountSvc()

user_service = UserSvc()

STATUS = ""
MESSAGE = ""

class VaquitaApp(App):
    """
    VaquitaApp is a textual app that displays a custom welcome message when started.
    """

    client = HttpClient()
    user_id = None

    def on_mount(self):
        # self.client.send('/readyz')
        # STATUS, MESSAGE = self.client.receive()
        #
        # print(f"Readyz check: {STATUS} - {MESSAGE}")

        def display_main_account(user_id):
            self.push_screen(CheckingAccountScreen(user_id))

        def display_main_menu(user_id):
            response_dict = self.client.send_request_and_get_response('/users/accounts/' + str(user_id))
            if response_dict:
                self.push_screen(CheckingAccountScreen(user_id))
            else:
                self.push_screen(ConfigCheckingAccountScreen(user_id), display_main_account)

        def check_form(form):
            if form == 'register':
                self.push_screen(screen=RegisterForm(), callback=display_main_menu)
            elif form == 'login':
                self.push_screen(screen=LoginForm(), callback=display_main_menu)

        self.push_screen(WelcomingScreen(), check_form)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to Vaquita!")

        yield Static(f"Readyz check: {STATUS} - {MESSAGE}")
        yield Footer()


app = VaquitaApp()
app.run()
