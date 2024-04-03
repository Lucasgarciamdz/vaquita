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

        new_user = self.user_repo.get_by_email(email)
        return new_user.id

    def login(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user is None:
            return False

        if user.check_password(password):
            return user.id

        return False

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_accounts(self, user_id):
        user = self.user_repo.get(user_id)
        return user.checking_accounts
