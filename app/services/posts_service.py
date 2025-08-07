from app.repositories.base_repository import PostsRepository

class PostsService:
    def __init__(self, posts_repository: PostsRepository):
        self.posts_repository = posts_repository

    def get_all(self):
        result = self.posts_repository.model.query.all()
        print(result)
        return result

    def get_by_id(self, post_id):
        return self.posts_repository.model.query.filter_by(post_id=post_id).first()