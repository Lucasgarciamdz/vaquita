from base_repo import BaseRepo
from vaquita.models.checking_account import CheckingAccountMdl
from vaquita.database.database_manager import DatabaseManager


db = DatabaseManager()

checking_account_session = db.session

class CheckingAccountRepo(BaseRepo):
    
    def __init__(self):
        super().__init__(CheckingAccountMdl, checking_account_session)

    def get_by_account_number(self, account_number):
        return self.session.query(CheckingAccountMdl).filter_by(account_number=account_number).first()
