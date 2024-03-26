"""This module contains a simple readiness controller that checks the database connection."""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from vaquita.database.database_manager import DatabaseManager

READYZ_FAIL_STATUS = 500
READYZ_OK_STATUS = 200
PATH_NOT_FOUND_STATUS = 404


class ReadyzController(BaseHTTPRequestHandler):
    """A simple readiness controller that checks the database connection."""

    def do_get(self) -> None:
        """Handle a GET request."""
        url = urlparse(self.path)
        if url.path == '/readyz':
            self.handle_readyz()
        else:
            self.send_response(PATH_NOT_FOUND_STATUS)
            self.end_headers()

    def handle_readyz(self) -> None:
        """Handle a readiness check."""
        db_manager = DatabaseManager()
        if db_manager.check_connection():
            self.send_response(READYZ_OK_STATUS)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(READYZ_FAIL_STATUS)
            self.end_headers()
            self.wfile.write(b'Database connection failed')
