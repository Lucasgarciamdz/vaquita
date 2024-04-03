from repositories.checking_account_repo import CheckingAccountRepo


class CheckingAccountSvc:
    def __init__(self):
        self.checking_account_repo = CheckingAccountRepo()

    def get_balance(self, account_name):
        account = self.checking_account_repo.get_by_account_name(account_name)
        return account.get_balance()

    def add_transaction(self, account_name, transaction):
        account = self.checking_account_repo.get_by_account_name(account_name)
        account.add_transaction(transaction)
        self.checking_account_repo.update_account(account)

    def get_transactions(self, account_name):
        account = self.checking_account_repo.get_by_account_name(account_name)
        return account.get_transactions()
