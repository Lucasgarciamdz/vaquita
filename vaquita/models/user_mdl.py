from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from models.bank.checking_account_mdl import user_account_association
from models.base_mdl import BaseMdl


class UserMdl(BaseMdl):
    """User model."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256))

    checking_accounts = relationship('CheckingAccountMdl', secondary=user_account_association, back_populates='users')
    transactions = relationship('TransactionMdl', back_populates='user')

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
