"""This module contains a simple readiness controller that checks the database connection."""

from logging import Logger

from config.logger_config import setup_custom_logger
from database.database_manager import DatabaseManager

READYZ_FAIL_STATUS = 500
READYZ_OK_STATUS = 200
PATH_NOT_FOUND_STATUS = 404

LOG: Logger = setup_custom_logger(__name__)


class ReadyzController:
    def do_GET(self, handler):
        LOG.info('Readyz controller')
        if handler.path == '/readyz':
            self.handle_readyz(handler)
        else:
            handler.send_response(PATH_NOT_FOUND_STATUS)
            handler.end_headers()

    def handle_readyz(self, handler):
        LOG.info('Checking database connection...')
        db_manager = DatabaseManager()
        if db_manager.check_connection():
            handler.send_response(READYZ_OK_STATUS)
            handler.end_headers()
            handler.wfile.write(b'OK')
            LOG.debug('Database connection successful')
        else:
            handler.send_response(READYZ_FAIL_STATUS)
            handler.end_headers()
            handler.wfile.write(b'Database connection failed')
            LOG.error('Database connection failed')
