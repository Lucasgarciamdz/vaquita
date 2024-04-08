from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship

from models.base_mdl import BaseMdl


class TransactionCategory(PyEnum):
    """Transaction categories."""
    FOOD = "Food"
    RENT = "Rent"
    SERVICES = "Services"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"
    HEALTH = "Health"
    INSURANCE = "Insurance"
    PERSONAL = "Personal"
    ENTERTAINMENT = "Entertainment"
    EDUCATION = "Education"
    SAVINGS = "Savings"
    SALARY = "Salary"


class TransactionType(PyEnum):
    """Transaction types."""
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"


class TransactionMdl(BaseMdl):
    """Transaction model."""

    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
    transaction_type = Column(Enum(TransactionType))
    category = Column(Enum(TransactionCategory))
    date = Column(DateTime)
    notes = Column(String)
    recurring = Column(Boolean)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    checking_account_id = Column(Integer, ForeignKey('checking_account.id'))

    checking_account = relationship('CheckingAccountMdl', back_populates='transactions')
    user = relationship('UserMdl', back_populates='transactions')

    def __repr__(self):
        return f'Transaction(id={self.id}, amount={self.amount},recurring={self.recurring}, transaction_type={self.transaction_type}, category={self.category}, user_id={self.user_id})'
