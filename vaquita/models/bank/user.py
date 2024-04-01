from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    """User model."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)

    checking_accounts = relationship('CheckingAccountMdl', back_populates='user')


    def set_password(self, password):
        """Hash the password and store the hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
