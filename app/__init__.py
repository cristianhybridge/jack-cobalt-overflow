# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask import Flask, render_template, url_for

# --- Inicialización de extensiones ---

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password", "wV9gEgOrK7XILhj3")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")
    
    # Construct the SQLAlchemy connection string
    # DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    # 
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    # If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
    # https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
    # engine = create_engine(DATABASE_URL, poolclass=NullPool)
    
    # Test the connection
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        
        
    @app.route('/')
    def home():
        return render_template('home.html')
        
    def login():
        return render_template('login.html')
    
    @app.route('/post')
    def post():
        return render_template('post.html')
    
    @app.route('/profile/<int:id>')
    def profile(id):
        return render_template('profile.html', user_id=id)
    
    return app
