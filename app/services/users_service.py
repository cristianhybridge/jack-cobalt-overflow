from app.repositories.base_repository import UsersRepository
from app.models.users_entity import Users, db

class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def get_all(self):
        return self.users_repository.model.query.all()

    def get_by_id(self, user_id):
        return self.users_repository.model.query.filter_by(user_id=user_id).first()

    def find_user_by_username(self, username: str) -> Users | None:
        if not username:
            return None
        return Users.query.filter_by(username=username).first()

    def create_user(self, username: str, password: str, email: str | None = None) -> Users:
        user = Users(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def verify_credentials(self, username: str, password: str) -> Users | None:
        user = self.find_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
