from datetime import timezone

from sqlalchemy import func

from app import db

class PostComment(db.Model):
    __tablename__ = 'post_comment'

    post_comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    commentary = db.Column(db.String(1000), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', backref='post_comment', lazy=True)

    def __repr__(self):
        return f"<post_comment {self.post_comment_id}: '{self.commentary}'>"