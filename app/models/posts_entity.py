from datetime import datetime, timezone

from app.database import db

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
    
    @hybrid_property
    def comments_count(self):
        from app.models.post_comment_entity import PostComment
        count = (db.session.query(func.count(PostComment.post_comment_id))
                 .filter(PostComment.post_id == self.post_id)
                 .scalar())
        print(f"[DEBUG] Post {self.post_id} -> comments_count = {count}")
        return count

    # Gracias a Gemini por esta maravilla de hybrid property
    @hybrid_property
    def time_since_creation(self):
        now = datetime.now(timezone.utc)

        # Ensure creation_date is timezone-aware
        creation = self.creation_date
        if creation.tzinfo is None:
            creation = creation.replace(tzinfo=timezone.utc)
            
        delta = now - creation

        seconds = int(delta.total_seconds())
        if seconds < 30:
            return f"Recién"
        elif seconds < 60:
            return f"Hace {seconds} segundo{'s' if seconds != 1 else ''}"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"Hace {minutes} minuto{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"Hace {hours} hora{'s' if hours != 1 else ''}"
        else:
            days = seconds // 86400
            return f"Hace {days} día{'s' if days != 1 else ''}"