from database.database_manager import DatabaseManager
from models.bank.transaction_mdl import TransactionMdl
from repositories.base_repo import BaseRepo

db = DatabaseManager()

transaction_session = db.session


class TransactionRepo(BaseRepo):

    def __init__(self):
        super().__init__(TransactionMdl, transaction_session)
