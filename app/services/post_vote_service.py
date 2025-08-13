from app.repositories.base_repository import PostVoteRepository

class PostVoteService:
    def __init__(self):
        self.posts_vote_repository = PostVoteRepository()

    def get_all(self):
        return self.posts_vote_repository.model.query.all()

    def get_by_id(self, post_vote_id):
        return self.posts_vote_repository.model.query.filter_by(post_vote_id=post_vote_id).first()

    def post_create(self, commentary):
        self.posts_vote_repository.model.commentary(commentary)