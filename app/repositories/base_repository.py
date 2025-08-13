from app.models.post_comment_entity import PostComment
from app.models.post_vote_entity import PostVote
from app.models.users_entity import Users
from app.models.posts_entity import Posts

class UsersRepository:
    def __init__(self):
        self.model = Users

class PostsRepository:
    def __init__(self):
        self.model = Posts
        
class PostCommentRepository:
    def __init__(self):
        self.model = PostComment
        
class PostVoteRepository:
    def __init__(self):
        self.model = PostVote