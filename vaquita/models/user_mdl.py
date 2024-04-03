from models.base_mdl import BaseMdl
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class UserMdl(BaseMdl):
    """User model."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256))

    checking_accounts = relationship('CheckingAccountMdl', back_populates='user')

    # Use a string to specify the relationship
    transactions = relationship('TransactionMdl', back_populates='user')

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
