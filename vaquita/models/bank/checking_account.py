from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CheckingAccountMdl(Base):

    __tablename__ = 'checking_account'

    id = Column(Integer, primary_key=True)
    account_number = Column(String)
    balance = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='checking_account')
    transactions = relationship('TransactionMdl', back_populates='checking_account')