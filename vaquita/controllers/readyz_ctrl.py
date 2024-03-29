"""This module contains a simple readiness controller that checks the database connection."""

from http.server import BaseHTTPRequestHandler
from logging import Logger
from urllib.parse import urlparse

from config.logger_config import setup_custom_logger
from database.database_manager import DatabaseManager

READYZ_FAIL_STATUS = 500
READYZ_OK_STATUS = 200
PATH_NOT_FOUND_STATUS = 404

LOG: Logger = setup_custom_logger(__name__)


class ReadyzController(BaseHTTPRequestHandler):
    """A simple readiness controller that checks the database connection."""

    def do_GET(self) -> None:  # pylint: disable=invalid-name # noqa: N802
        """Handle a GET request."""
        LOG.info('Readyz controller')
        url = urlparse(self.path)
        if url.path == '/readyz':
            self.handle_readyz()
        else:
            self.send_response(PATH_NOT_FOUND_STATUS)
            self.end_headers()

    def handle_readyz(self) -> None:  # noqa: WPS213
        """Handle a readiness check."""
        LOG.info('Checking database connection...')
        db_manager = DatabaseManager()
        if db_manager.check_connection():
            self.send_response(READYZ_OK_STATUS)
            self.end_headers()
            self.wfile.write(b'OK')
            LOG.debug('Database connection successful')
        else:
            self.send_response(READYZ_FAIL_STATUS)
            self.end_headers()
            self.wfile.write(b'Database connection failed')
            LOG.error('Database connection failed')
