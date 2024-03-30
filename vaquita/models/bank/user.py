from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    
        __tablename__ = 'user'
    
        id = Column(Integer, primary_key=True)
        name = Column(String)
        email = Column(String)
        password = Column(String)
        checking_account = relationship('CheckingAccount', back_populates='user')
        savings_account = relationship('SavingsAccount', back_populates='user')
    
        def __repr__(self):
            return f'User(id={self.id}, name={self.name}, email={self.email})'