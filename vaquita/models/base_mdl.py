# base_mdl.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseMdl(Base):
    """Base class for all models."""

    __abstract__ = True

    def as_dict(self):
        """Return the model as a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
