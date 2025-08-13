from app.repositories.base_repository import PostCommentRepository

class PostCommentService:
    def __init__(self):
        self.posts_comment_repository = PostCommentRepository()

    def get_all(self):
        return self.posts_comment_repository.model.query.all()

    def get_by_id(self, post_comment_id):
        return self.posts_comment_repository.model.query.filter_by(post_comment_id=post_comment_id).first()

    def post_create(self, commentary):
        self.posts_comment_repository.model.commentary(commentary)