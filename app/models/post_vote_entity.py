from datetime import timezone

from sqlalchemy import func, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class PostVote(db.Model):
    __tablename__ = 'post_vote'

    post_vote_id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, ForeignKey('posts.post_id'), nullable=False)
    created_by = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)

    __table_args__ = (UniqueConstraint('post_id', 'created_by'),)

    vote = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<post_vote {self.post_vote_id}: Post id: '{self.post_id}' / Created by: '{self.created_by}'>"

