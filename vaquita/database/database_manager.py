"""Database setup for the Vaquita application."""
import configparser
from typing import Optional

from sqlalchemy import create_engine, exc
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

properties = configparser.ConfigParser()
properties.read('vaquita/vaquita.properties')

DATABASE_URL = properties['DATABASE']['url']


class DatabaseManager:
    """A singleton class that manages a database using SQLAlchemy."""

    _instance: Optional['DatabaseManager'] = None
    _session: Optional[scoped_session] = None
    engine: Engine
    session_factory: sessionmaker

    def __new__(cls) -> 'DatabaseManager':
        """
        Ensure only one instance of the class can be created.

        Returns:
            DatabaseManager: The singleton instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the database manager with the given database URL."""
        self.engine = create_engine(DATABASE_URL)
        self.session_factory = sessionmaker(bind=self.engine)

    @property
    def session(self) -> scoped_session:
        """
        Return a singleton session. If no session exists, one is created.

        Returns:
            scoped_session: The singleton session.
        """
        if self._session is None:
            self._session = scoped_session(self.session_factory)
        return self._session

    def create_database(self) -> None:
        """Create all tables in the database."""
        Base.metadata.create_all(self.engine)

    def delete_database(self) -> None:
        """Drop all tables in the database."""
        Base.metadata.drop_all(self.engine)

    def check_connection(self) -> bool:
        """
        Check the database connection.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            with self.engine.connect() as connection:
                connection_status = connection.execute('SELECT 1')
                return connection_status.scalar() == 1
        except exc.SQLAlchemyError:
            return False
