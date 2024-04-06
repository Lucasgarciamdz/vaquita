from models.base_mdl import BaseMdl, user_account_association
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, MetaData
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

metadata = MetaData()


class CheckingAccountMdl(BaseMdl):
    """Checking account model."""

    __tablename__ = 'checking_account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_number = Column(String)
    balance = Column(Numeric)
    password_hash = Column(String)

    users = relationship('UserMdl', secondary=user_account_association, back_populates='checking_accounts')
    transactions = relationship('TransactionMdl', back_populates='checking_account')

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'CheckingAccount(id={self.id}, account_number={self.account_number}, balance={self.balance}, user_id={self.user_id})'
