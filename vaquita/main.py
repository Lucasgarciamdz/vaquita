import json
import threading
from pprint import pprint
from queue import Queue, Empty
from socket_client import SocketClient
from termcolor import colored

class VaquitaApp:
    def __init__(self):
        self.client = SocketClient()
        self.user_id = None
        self.transactions = []
        self.update_queue = Queue()
        self.running = True
        self.account_id = 1

        # Start the update listener thread
        self.update_listener_thread = threading.Thread(target=self.listen_for_updates, daemon=True)
        self.update_listener_thread.start()

    def run(self):
        print(colored("Welcome to Vaquita!", "cyan", attrs=["bold"]))
        while self.running:
            if not self.user_id:
                self.show_welcome_screen()
            else:
                self.show_main_menu()

    def listen_for_updates(self):
        while self.running:
            try:
                data = self.client.sock.recv(16384).decode("utf-8")
                if data:
                    for line in data.strip().split("\n"):
                        update = json.loads(line)
                        self.update_queue.put(update)
            except Exception as e:
                print(f"Error receiving updates: {e}")

    def handle_update(self, update):
        if update.get("type") == "transaction_update":
            self.transactions.append(update["transaction"])
            print(colored("\nNew transaction received:", "green", attrs=["bold"]))
            pprint(update["transaction"])
            print(colored("\nUpdated Transactions:", "yellow", attrs=["bold"]))
            self.print_transactions(self.transactions)

    def view_selected_account(self, account):
        print(colored(f"\nViewing Account: {account['name']} - {account['account_number']}", "cyan", attrs=["bold"]))
        self.transactions = account.get('transactions', [])
        self.print_transactions(self.transactions)

        # Start the update listener thread for the selected account
        self.selected_account_running = True
        self.selected_account_thread = threading.Thread(target=self.listen_for_account_updates, args=(account['id'],), daemon=True)
        self.selected_account_thread.start()

        while self.selected_account_running:
            print(colored("\nOptions:", "blue"))
            print(colored("1. Refresh Transactions", "blue"))
            print(colored("2. Add Transaction", "blue"))
            print(colored("3. Back to Main Menu", "blue"))

            choice = input(colored("Enter your choice: ", "cyan"))
            if choice == "1":
                self.view_transactions(account['id'])
            elif choice == "2":
                self.add_transaction_to_account(account['id'])
            elif choice == "3":
                self.selected_account_running = False
            else:
                print(colored("Invalid choice. Please try again.", "red"))

    def listen_for_account_updates(self, account_id):
        while self.selected_account_running:
            try:
                update = self.update_queue.get(timeout=1)
                self.handle_account_update(update, account_id)
            except Empty:
                continue

    def handle_account_update(self, update, account_id):
        if update.get("type") == "transaction_update" and update["transaction"]["checking_account_id"] == account_id:
            self.transactions.append(update["transaction"])
            print(colored("\nNew transaction received:", "green", attrs=["bold"]))
            pprint(update["transaction"])
            print(colored("\nUpdated Transactions:", "yellow", attrs=["bold"]))
            self.print_transactions(self.transactions)
        elif update.get("type") == "balance_update" and update["account_id"] == account_id:
            print(colored(f"\nBalance updated: {update['new_balance']}", "green", attrs=["bold"]))

    def show_welcome_screen(self):
        print("\n" + colored("1. Register", "blue"))
        print(colored("2. Login", "blue"))
        print(colored("3. Quit", "blue"))
        choice = input(colored("Enter your choice: ", "cyan"))
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            self.running = False
            print(colored("Goodbye!", "red"))
        else:
            print(colored("Invalid choice. Please try again.", "red"))

    def register(self):
        name = input(colored("Enter your name: ", "cyan"))
        email = input(colored("Enter your email: ", "cyan"))
        password = input(colored("Enter your password: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/users/register",
            "POST",
            {"name": name, "email": email, "password": password}
        )
        if response and "user_id" in response:
            self.user_id = response["user_id"]
            print(colored("Registration successful!", "green"))
        else:
            print(colored("Registration failed. Please try again.", "red"))

    def login(self):
        email = input(colored("Enter your email: ", "cyan"))
        password = input(colored("Enter your password: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/users/login",
            "POST",
            {"email": email, "password": password}
        )
        if response and "user_id" in response:
            self.user_id = response["user_id"]
            print(colored("Login successful!", "green"))
        else:
            print(colored("Login failed. Please try again.", "red"))

    def show_main_menu(self):
        print("\n" + colored("1. View Accounts", "blue"))
        print(colored("2. Create Personal Bank", "blue"))
        print(colored("3. Create Vaquita", "blue"))
        print(colored("4. Join Vaquita", "blue"))
        print(colored("5. Add Transaction", "blue"))
        print(colored("6. View Transactions", "blue"))
        print(colored("7. Select Account", "blue"))
        print(colored("8. Logout", "blue"))
        choice = input(colored("Enter your choice: ", "cyan"))
        if choice == "1":
            self.view_accounts()
        elif choice == "2":
            self.create_personal_bank()
        elif choice == "3":
            self.create_vaquita()
        elif choice == "4":
            self.join_vaquita()
        elif choice == "5":
            self.add_transaction()
        elif choice == "6":
            self.view_transactions(self.account_id)
        elif choice == "7":
            self.select_account()
        elif choice == "8":
            self.user_id = None
            print(colored("Logged out successfully.", "green"))
        else:
            print(colored("Invalid choice. Please try again.", "red"))

    def view_accounts(self):
        response = self.client.send_request_and_get_response(
            f"/users/accounts/{self.user_id}",
            "GET"
        )
        if response:
            print("\n" + colored("Your Accounts:", "yellow", attrs=["bold"]))
            pprint(response)
        else:
            print(colored("Failed to retrieve accounts.", "red"))

    def select_account(self):
        response = self.client.send_request_and_get_response(
            f"/users/accounts/{self.user_id}",
            "GET"
        )
        if response:
            print("\n" + colored("Your Accounts:", "yellow", attrs=["bold"]))
            for i, account in enumerate(response, 1):
                print(f"{i}. Name: {account['name']}, Balance: {account['balance']}, Account Number: {account['account_number']}")

            choice = input(colored("Select an account by number: ", "cyan"))
            try:
                choice = int(choice) - 1
                selected_account = response[choice]
                print(colored(f"Selected Account: {selected_account['name']} - {selected_account['account_number']}", "green"))
                self.account_id = selected_account['id']
                self.view_selected_account(selected_account)
            except (ValueError, IndexError):
                print(colored("Invalid choice. Please try again.", "red"))
        else:
            print(colored("Failed to retrieve accounts.", "red"))

    def view_transactions(self, account_id):
        response = self.client.send_request_and_get_response(
            f"/checking_accounts/transactions/{account_id}",
            "GET"
        )
        if response:
            self.transactions = response
            print("\n" + colored("Transactions:", "yellow", attrs=["bold"]))
            self.print_transactions(self.transactions)
        else:
            print(colored("Failed to retrieve transactions.", "red"))

    def add_transaction_to_account(self, account_id):
        amount = input(colored("Enter amount: ", "cyan"))
        transaction_type = input(colored("Enter transaction type (INCOME, EXPENSE, TRANSFER): ", "cyan"))
        category = input(colored("Enter category (FOOD, RENT, SERVICES, etc.): ", "cyan"))
        description = input(colored("Enter description: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/checking_accounts/transactions/add",
            "POST",
            {
                "account_id": account_id, "amount": amount, "transaction_type": transaction_type,
                "category": category, "description": description, "user_id": self.user_id
            }
        )
        if response:
            print(colored("Transaction added successfully!", "green"))
        else:
            print(colored("Failed to add transaction.", "red"))

    def create_personal_bank(self):
        name = input(colored("Enter bank name: ", "cyan"))
        balance = input(colored("Enter initial balance: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/users/create_personal_bank",
            "POST",
            {"bank_name": name, "bank_balance": balance, "user_id": self.user_id, "password": "password"}
        )
        if response:
            print(colored("Personal bank created successfully!", "green"))
        else:
            print(colored("Failed to create personal bank.", "red"))

    def create_vaquita(self):
        name = input(colored("Enter Vaquita name: ", "cyan"))
        balance = input(colored("Enter initial balance: ", "cyan"))
        password = input(colored("Enter Vaquita password: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/users/create_vaquita",
            "POST",
            {"bank_name": name, "bank_balance": balance, "user_id": self.user_id, "password": password}
        )
        if response:
            print(colored("Vaquita created successfully!", "green"))
        else:
            print(colored("Failed to create Vaquita.", "red"))

    def join_vaquita(self):
        account_number = input(colored("Enter Vaquita account number: ", "cyan"))
        password = input(colored("Enter Vaquita password: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/users/join_vaquita",
            "POST",
            {"user_id": self.user_id, "vaquita_number": account_number, "password": password}
        )
        if response and response.get("result"):
            print(colored("Joined Vaquita successfully!", "green"))
        else:
            print(colored("Failed to join Vaquita.", "red"))

    def add_transaction(self):
        account_id = input(colored("Enter account ID: ", "cyan"))
        amount = input(colored("Enter amount: ", "cyan"))
        transaction_type = input(colored("Enter transaction type (INCOME, EXPENSE, TRANSFER): ", "cyan"))
        category = input(colored("Enter category (FOOD, RENT, SERVICES, etc.): ", "cyan"))
        description = input(colored("Enter description: ", "cyan"))
        response = self.client.send_request_and_get_response(
            "/checking_accounts/transactions/add",
            "POST",
            {
                "account_id": account_id, "amount": amount, "transaction_type": transaction_type,
                "category": category, "description": description, "user_id": self.user_id
            }
        )
        if response:
            print(colored("Transaction added successfully!", "green"))
        else:
            print(colored("Failed to add transaction.", "red"))

    def print_transactions(self, transactions):
        if not transactions:
            print("No transactions found.")
            return

        print("\nTransactions:")
        print("-" * 80)
        print(f"{'Date':<20}{'Type':<10}{'Category':<15}{'Amount':<10}{'Description':<25}")
        print("-" * 80)

        for transaction in transactions:
            date = transaction['date']
            transaction_type = transaction['transaction_type'].capitalize()
            category = transaction['category'].capitalize()
            amount = f"${transaction['amount']:.2f}"
            description = transaction['description'][:25]  # Truncate description if too long

            print(f"{date:<20}{transaction_type:<10}{category:<15}{amount:<10}{description:<25}")

        print("-" * 80)

if __name__ == "__main__":
    app = VaquitaApp()
    app.run()
