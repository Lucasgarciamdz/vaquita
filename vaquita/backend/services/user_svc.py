from backend.models.user_mdl import UserMdl
from backend.repositories.user_repo import UserRepo
from backend.services.checking_account_svc import CheckingAccountSvc

checking_account_service = CheckingAccountSvc()


class UserSvc:
    def __init__(self):
        self.user_repo = UserRepo()

    def register(self, name, email, password):
        user = UserMdl(name=name, email=email)
        user.set_password(password)
        self.user_repo.add(user)
        new_user = self.user_repo.get_by_email(email)
        return new_user.id

    def create_vaquita(self, bank_name, bank_balance, user_id, password):
        user = self.user_repo.get(user_id)
        checking_account_service.create_account(
            bank_name, bank_balance, user, password, personal=False
        )

    def join_vaquita(self, user_id, vaquita_number, password):
        user = self.user_repo.get(user_id)
        return checking_account_service.join_account(vaquita_number, user, password)

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

    def create_personal_bank(
        self, bank_name, bank_balance, user_id, password, personal=True
    ):
        user = self.user_repo.get(user_id)
        checking_account_service.create_account(
            bank_name, bank_balance, user, password, personal
        )
