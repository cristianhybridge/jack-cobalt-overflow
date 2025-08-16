from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import db
class PostComment(db.Model):
    __tablename__ = 'post_comment'

    post_comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    commentary = db.Column(db.String(5000), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    creator = db.relationship('Users', backref='post_comment', lazy=True)

    def __repr__(self):
        return f"<post_comment {self.post_comment_id}: '{self.commentary}'>"

    @hybrid_property
    def time_since_creation(self):
        now = datetime.now(timezone.utc)

        # Ensure creation_date is timezone-aware
        creation = self.creation_date
        if creation.tzinfo is None:
            creation = creation.replace(tzinfo=timezone.utc)

        delta = now - creation

        seconds = int(delta.total_seconds())
        if seconds < 5:
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