"""Main module to run the server."""
from http.server import HTTPServer

from controllers.readyz_ctrl import ReadyzController
from database.database_manager import DatabaseManager
from config.logger_config import setup_custom_logger

LOG = setup_custom_logger(__name__)

def run(server_class=HTTPServer, handler_class=ReadyzController, port=8000):
    """Run the server."""
    LOG.info('Starting the server...')
    DatabaseManager().create_database()
    
    LOG.info('Database created.')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
