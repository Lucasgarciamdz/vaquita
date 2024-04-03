from models.user_mdl import UserMdl
from repositories.user_repo import UserRepo


class UserSvc():

    def __init__(self):
        self.user_repo = UserRepo()

    def register(self, name, email, password):
        user = UserMdl()
        user.name = name
        user.email = email
        user.set_password(password)
        self.user_repo.add(user)

    def login(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user is None:
            return False

        return user.check_password(password)

    def get_all_users(self):
        return self.user_repo.get_all()
