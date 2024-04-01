from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CheckingAccount(Base):
    __tablename__ = 'checking_account'

    id = Column(Integer, primary_key=True)
    incomes = Column(Float)
    expenses = Column(Float)
    balance = Column(Float)
    transactions = relationship('TransactionDTO', back_populates='checking_account')

    def available_balance(self):
        return self.balance

    def new_transaction(self, transaction_dto):
        # Add your transaction logic here
        pass