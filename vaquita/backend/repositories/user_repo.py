from backend.database.database_manager import DatabaseManager
from backend.models.user_mdl import UserMdl
from backend.repositories.base_repo import BaseRepo

db = DatabaseManager()

user_repo_session = db.session


class UserRepo(BaseRepo):
    def __init__(self):
        super().__init__(UserMdl, user_repo_session)

    def get_by_email(self, email):
        return self.session.query(UserMdl).filter_by(email=email).first()
