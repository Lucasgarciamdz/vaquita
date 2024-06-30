import multiprocessing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from statistics import StatisticsSvc, StatisticsRepo


def statistics_process(queue, event):
    # Set up the database session
    engine = create_engine("sqlite:///statistics.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Set up the statistics service and repository
    statistics_repo = StatisticsRepo(session)
    statistics_service = StatisticsSvc(statistics_repo)

    while True:
        event.wait()  # Wait for the event to be set
        event.clear()  # Clear the event
        message = queue.get()
        if message == "data_saved":
            # Perform the calculations
            totals = statistics_service.calculate_totals()
            averages = statistics_service.calculate_averages()
            largest = statistics_service.calculate_largest()
            category_percentages = statistics_service.calculate_category_percentages()

            # Print the results (you can replace this with whatever you want to do with the results)
            print("Totals:", totals)
            print("Averages:", averages)
            print("Largest:", largest)
            print("Category percentages:", category_percentages)


if __name__ == "__main__":
    # Create the queue and the event
    queue = multiprocessing.Queue()
    event = multiprocessing.Event()

    # Start the statistics process
    p = multiprocessing.Process(target=statistics_process, args=(queue, event))
    p.start()

    # Simulate the server saving data in the database and informing the statistics process
    queue.put("data_saved")
    event.set()  # Set the event

    # Wait for the statistics process to finish (in a real application, you would probably want to keep the server running indefinitely)
    p.join()
