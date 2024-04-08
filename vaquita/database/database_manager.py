"""Database setup for the Vaquita application."""
import os
from logging import Logger
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import DDL
from sqlalchemy import create_engine, exc, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config.logger_config import setup_custom_logger
from models.base_mdl import BaseMdl

# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file
env_path = os.path.join(script_dir, '../properties/.env')

# Load the .env file
load_dotenv(env_path)
DATABASE_URL: str = os.getenv('DATABASE_URL', 'not set')

LOG: Logger = setup_custom_logger(__name__)


class DatabaseManager:  # noqa: WPS306
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
        LOG.info('Creating database...')
        BaseMdl.metadata.create_all(self.engine)

    def delete_database(self) -> None:
        """Drop all tables in the database."""
        LOG.info('Deleting database...')
        with self.engine.begin() as connection:
            for table in reversed(BaseMdl.metadata.sorted_tables):
                connection.execute(DDL(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))

    def check_connection(self) -> bool:
        """
        Check the database connection.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            with self.engine.connect() as connection:
                LOG.info('Checking database connection...')
                connection_status = connection.execute(text('SELECT 1'))
                return connection_status.scalar() == 1
        except exc.SQLAlchemyError:
            LOG.error('Database connection failed.', exc_info=True)
            return False
