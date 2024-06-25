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
            self.send_response(handler, PATH_NOT_FOUND_STATUS)

    def handle_readyz(self, handler):
        LOG.info('Checking database connection...')
        db_manager = DatabaseManager()
        if db_manager.check_connection():
            self.send_response(handler, READYZ_OK_STATUS, b'OK')
            LOG.debug('Database connection successful')
        else:
            self.send_response(handler, READYZ_FAIL_STATUS, b'Database connection failed')
            LOG.error('Database connection failed')

    def send_response(self, handler, status_code, body=b''):
        handler.send_response(status_code)
        handler.send_header('Content-Length', str(len(body)))
        handler.end_headers()
        if body:
            handler.wfile.write(body)
