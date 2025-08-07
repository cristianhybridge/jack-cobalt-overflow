from app import db

# Define el modelo de usuario
class Posts(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    commentary = db.Column(db.String(1000), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # Corregimos el __repr__ para que coincida con las columnas
        return f"Post('{self.post_id}', '{self.commentary}')"