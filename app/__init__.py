from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
import os
from dotenv import load_dotenv


# --- Inicialización de extensiones fuera del create_app ---
db = SQLAlchemy()
migrate = Migrate()

from app.services.posts_service import PostsService

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY') or 'a-very-secret-key'

    # ------------------ SQL Connection   
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    dbname = os.getenv("dbname")

    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ------------------ Endpoint Routing
    @app.route('/')
    def home():
        from app.models import Posts
        posts = db.session.query(Posts).all()
        for post in posts:
            print(f"Debug votes: {post.votes}")
        
        return render_template('home.html', posts=posts)
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/post/<int:id>')
    def post(id):
        from app.models import Posts
        post = Posts.query.get_or_404(id)
        return render_template('post.html', post=post)

    @app.route('/post/new')
    def new_post():
        return render_template('new_post.html')

    @app.route('/profile/<int:id>')
    def profile(id):
        return render_template('profile.html', user_id=id)

    # --- Initialize extensions WITH the app instance ---
    db.init_app(app)
    migrate.init_app(app, db)

    # Test the connection
    try:
        from sqlalchemy import create_engine
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")

    # ------------------ Endpoint Routing & Resources
    from app.routes.users_routes import UserRoutes
    UserRoutes(app)
    
    from app.routes.posts_routes import PostRoutes
    PostRoutes(app)
    
    from app.routes.post_vote_routes import PostVoteRoutes
    PostVoteRoutes(app)
    
    from app.routes.post_comment_routes import PostCommentRoutes
    PostCommentRoutes(app)

    # ------------------

    return app

