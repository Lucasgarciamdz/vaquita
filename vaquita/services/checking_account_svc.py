from vaquita.repositories.checking_account_repo import CheckingAccountRepo


class CheckingAccountSvc:
    def __init__(self):
        self.checking_account_repo = CheckingAccountRepo()

    def deposit(self, account_name, amount):
        account = self.checking_account_repo.get_account(account_name)
        account.deposit(amount)
        self.checking_account_repo.update_account(account)

    def withdraw(self, account_name, amount):
        account = self.checking_account_repo.get_account(account_name)
        account.withdraw(amount)
        self.checking_account_repo.update_account(account)

    def get_balance(self, account_name):
        account = self.checking_account_repo.get_account(account_name)
        return account.get_balance()

    def add_transaction(self, account_name, transaction):
        account = self.checking_account_repo.get_account(account_name)
        account.add_transaction(transaction)
        self.checking_account_repo.update_account(account)

    def get_transactions(self, account_name):
        account = self.checking_account_repo.get_account(account_name)
        return account.get_transactions()