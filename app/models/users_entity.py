from app import db
from flask_login import UserMixin

# Define el modelo de usuario
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        # Corregimos el __repr__ para que coincida con las columnas
        return self.nickname