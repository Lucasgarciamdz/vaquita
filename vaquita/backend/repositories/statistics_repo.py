from base_repo import BaseRepo
from backend.database.database_manager import DatabaseManager
from backend.models.statistics.statistics_mdl import StatisticsMdl

db = DatabaseManager()

statistics_session = db.session


class StatisticsRepo(BaseRepo):
    def __init__(self):
        super().__init__(StatisticsMdl, statistics_session)
