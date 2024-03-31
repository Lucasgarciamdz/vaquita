from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class CheckingAccountMdl(Base):
    """Checking account model."""

    __tablename__ = 'checking_account'

    id = Column(Integer, primary_key=True)
    account_number = Column(String)
    balance = Column(Numeric)
    user_id = Column(Integer, ForeignKey('user.id'))
    password_hash = Column(String)

    user = relationship('User', back_populates='checking_accounts')
    transactions = relationship('TransactionMdl', back_populates='checking_account')


    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'CheckingAccount(id={self.id}, account_number={self.account_number}, balance={self.balance}, user_id={self.user_id})'