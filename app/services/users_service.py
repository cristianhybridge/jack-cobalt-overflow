from app.repositories.base_repository import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository
        
    def get_all(self):
        result = self.users_repository.model.query.all()
        print(result)
        return result
    
    def get_by_id(self, user_id):
        return self.users_repository.model.query.filter_by(user_id=user_id).first()