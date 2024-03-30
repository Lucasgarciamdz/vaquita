from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class StatsMdl(Base):

    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='stats')
    transactions = relationship('TransactionMdl', back_populates='stats')