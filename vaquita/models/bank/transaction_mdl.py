from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TransactionMdl(Base):
    
        __tablename__ = 'transaction'
    
        id = Column(Integer, primary_key=True)
        amount = Column(Integer)
        transaction_type = Column(String)
        category = Column(String)
        checking_account_id = Column(Integer, ForeignKey('checking_account.id'))
    
        checking_account = relationship('CheckingAccountMdl', back_populates='transactions')
    
        def __repr__(self):
            return f'Transaction(id={self.id}, amount={self.amount}, transaction_type={self.transaction_type})'
