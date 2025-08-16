from app.database import db

class Hints(db.Model):
    __tablename__ = 'hints'

    hint_id = db.Column(db.Integer, primary_key=True)
    hint = db.Column(db.String(1000), nullable=False)
    def __repr__(self):
        return f"Hint('{self.hint_id}', '{self.hint}')"