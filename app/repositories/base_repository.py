from app.models.users_entity import Users
from app.models.posts_entity import Posts

class UsersRepository:
    def __init__(self):
        self.model = Users

class PostsRepository:
    def __init__(self):
        self.model = Posts