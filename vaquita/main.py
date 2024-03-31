import multiprocessing
from vaquita.database.database_manager import DatabaseManager
from vaquita.server import ServerSvc
from vaquita.statistics import StatisticsSvc

def main():
    """Main function."""
    db_manager = DatabaseManager()
    db_manager.create_database()
    db_manager.create_tables()

    # Create a process for the server
    server_process = multiprocessing.Process(target=ServerSvc().start)
    server_process.start()

    # Create a process for the statistics service
    statistics_process = multiprocessing.Process(target=StatisticsSvc().start)
    statistics_process.start()

    # Wait for all processes to finish
    server_process.join()
    statistics_process.join()

if __name__ == "__main__":
    main()