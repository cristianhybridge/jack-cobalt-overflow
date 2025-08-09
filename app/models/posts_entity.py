from datetime import timezone

from sqlalchemy import func

from app import db

# Define el modelo de usuario
class Posts(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    commentary = db.Column(db.String(1000), nullable=False)
    affected_area = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    upvotes = db.Column(db.Integer, nullable=True)
    downvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    expiration_date = db.Column(db.DateTime(timezone=True), nullable=False)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', backref='posts', lazy=True)

    def __repr__(self):
        return f"<Post {self.post_id}: '{self.title}'>"