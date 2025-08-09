from app.repositories.base_repository import PostsRepository

class PostsService:
    def __init__(self):
        self.posts_repository = PostsRepository()

    def get_all(self):
        return self.posts_repository.model.query.all()

    def get_by_id(self, post_id):
        return self.posts_repository.model.query.filter_by(post_id=post_id).first()
    
    def post_create(self, post):
        self.posts_repository.model.post(post)