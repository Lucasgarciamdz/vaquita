# base_mdl.py
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()
user_account_association = Table('user_account_association', metadata,
                                 Column('user_id', Integer, ForeignKey('user.id')),
                                 Column('account_id', Integer, ForeignKey('checking_account.id'))
                                 )

class BaseMdl(Base):
    """Base class for all models."""

    __abstract__ = True

    def as_dict(self):
        """Return the model as a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
