from base_repo import BaseRepo
from vaquita.database.database_manager import DatabaseManager
from vaquita.models.statistics.statistics_mdl import StatisticsMdl

db = DatabaseManager()

statistics_session = db.session


class StatisticsRepo(BaseRepo):

    def __init__(self):
        super().__init__(StatisticsMdl, statistics_session)
