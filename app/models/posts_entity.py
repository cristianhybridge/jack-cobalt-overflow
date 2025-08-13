from datetime import timezone

from sqlalchemy import func

from app import db

# Define el modelo de usuario
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select

class Posts(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    commentary = db.Column(db.String(1000), nullable=False)
    affected_area = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    expiration_date = db.Column(db.DateTime(timezone=True), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', backref='posts', lazy=True)

    @hybrid_property
    def votes(self):
        from app.models.post_vote_entity import PostVote
        count = db.session.query(func.count(PostVote.post_vote_id)) \
            .filter(PostVote.post_id == self.post_id) \
            .scalar()
        print(f"[DEBUG] Post {self.post_id} -> votos = {count}")
        return count


    # @votes.expression
    # def votes(cls):
    #     from app.models.post_vote_entity import PostVote
    #     return (
    #         select(func.count(PostVote.post_vote_id))
    #         .where(PostVote.post_id == cls.post_id)
    #         .correlate(cls)
    #         .scalar_subquery()
    #     )
