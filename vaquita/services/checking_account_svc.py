from repositories.checking_account_repo import CheckingAccountRepo
import random
from models.bank.checking_account_mdl import CheckingAccountMdl
import string


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

    def create_account(self, name, balance, user_id, password):
        new_account = CheckingAccountMdl()
        new_account.name = name
        new_account.account_number = '#' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        new_account.balance = balance
        new_account.user_id = user_id
        new_account.set_password(password)
        self.checking_account_repo.add(new_account)

    def join_account(self, account_number, user_id):
        account = self.checking_account_repo.get_by_account_number(account_number)
        account.user_id = user_id
        self.checking_account_repo.update_account(account)