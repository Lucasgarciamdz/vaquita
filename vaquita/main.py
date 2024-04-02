from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button

from terminal_ui.welcoming_tui import WelcomingScreen
from terminal_ui.user_tui import RegisterForm, LoginForm



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

    def compose(self) -> ComposeResult:
        yield Header()

        yield Footer()


app = VaquitaApp()
app.run()
