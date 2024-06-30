from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Table, MetaData
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from models.base_mdl import BaseMdl

metadata = MetaData()

user_account_association = Table(
    "user_account_association",
    BaseMdl.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("account_id", Integer, ForeignKey("checking_account.id")),
)


class CheckingAccountMdl(BaseMdl):
    """Checking account model."""

    __tablename__ = "checking_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_number = Column(String)
    balance = Column(Numeric)
    password_hash = Column(String)

    users = relationship(
        "UserMdl",
        secondary=user_account_association,
        back_populates="checking_accounts",
    )
    transactions = relationship("TransactionMdl", back_populates="checking_account")

    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"CheckingAccount(id={self.id}, account_number={self.account_number}, balance={self.balance}"

    def to_dict(self, depth=1):
        if depth < 0:
            return self.id
        return {
            "id": self.id,
            "name": self.name,
            "account_number": self.account_number,
            "balance": float(self.balance),
            "users": [user.to_dict(depth - 1) for user in self.users]
            if depth > 0
            else None,
            "transactions": [
                transaction.to_dict(depth - 1) for transaction in self.transactions
            ]
            if depth > 0
            else None,
        }
