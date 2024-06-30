import random
import string
from datetime import datetime

from models.bank.checking_account_mdl import CheckingAccountMdl
from models.bank.transaction_mdl import (
    TransactionMdl,
    TransactionType,
    TransactionCategory,
)
from repositories.checking_account_repo import CheckingAccountRepo
from repositories.transaction_repo import TransactionRepo


class CheckingAccountSvc:
    def __init__(self):
        self.checking_account_repo = CheckingAccountRepo()
        self.transaction_repo = TransactionRepo()

    def get_balance(self, account_name):
        account = self.checking_account_repo.get_by_account_name(account_name)
        return account.get_balance()

    def add_transaction(
        self,
        account_id,
        amount,
        transaction_type,
        category,
        notes,
        recurring,
        description,
        user_id,
    ):
        account = self.checking_account_repo.get(account_id)
        if account is None:
            raise ValueError("Account not found for id: " + str(account_id))
        transaction = TransactionMdl(
            amount=amount,
            transaction_type=TransactionType[transaction_type],
            category=TransactionCategory[category],
            date=datetime.now(),
            notes=notes,
            recurring=recurring,
            description=description,
            user_id=user_id,
            checking_account_id=account.id,
        )
        self.transaction_repo.add(transaction)
        account.transactions.append(transaction)
        self.checking_account_repo.update(account)

    def get_transactions(self, account_id):
        account = self.checking_account_repo.get(account_id)
        return account.transactions

    def create_account(self, name, balance, user, password, personal=True):
        new_account = CheckingAccountMdl()
        new_account.name = name
        if not personal:
            new_account.account_number = "#" + "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(5)
            )
            new_account.set_password(password)
        new_account.balance = balance
        new_account.users = [user]
        self.checking_account_repo.add(new_account)

    def join_account(self, account_number, user, account_password):
        account = self.checking_account_repo.get_by_account_number(account_number)
        if account is None or not account.check_password(account_password):
            return False
        account.users.append(user)
        self.checking_account_repo.update(account)
        return True
