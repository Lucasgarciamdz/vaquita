from database.database_manager import DatabaseManager
from repositories.base_repo import BaseRepo
from models.bank.transaction_mdl import TransactionMdl

db = DatabaseManager()

transaction_session = db.session


class TransactionRepo(BaseRepo):

    def __init__(self):
        super().__init__(TransactionMdl, transaction_session)