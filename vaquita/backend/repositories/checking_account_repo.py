from database.database_manager import DatabaseManager
from models.bank.checking_account_mdl import CheckingAccountMdl
from repositories.base_repo import BaseRepo

db = DatabaseManager()

checking_account_session = db.session


class CheckingAccountRepo(BaseRepo):
    def __init__(self):
        super().__init__(CheckingAccountMdl, checking_account_session)

    def get_by_account_number(self, account_number):
        return (
            self.session.query(CheckingAccountMdl)
            .filter_by(account_number=account_number)
            .first()
        )

    def get_by_account_name(self, account_name):
        return (
            self.session.query(CheckingAccountMdl).filter_by(name=account_name).first()
        )
