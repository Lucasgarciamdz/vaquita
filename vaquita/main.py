import multiprocessing
from vaquita.terminal_ui.bank_tui import BankApp
from vaquita.terminal_ui.checking_account_tui import CheckingAccountApp
from vaquita.server import start_server

def main():
    # Create a process for the banking application
    bank_process = multiprocessing.Process(target=BankApp.run)
    bank_process.start()

    # Create a process for the checking account application
    checking_account_process = multiprocessing.Process(target=CheckingAccountApp.run)
    checking_account_process.start()

    # Start the server
    start_server()

if __name__ == "__main__":
    main()