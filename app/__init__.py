from flask import Flask, render_template, g
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
import os
from dotenv import load_dotenv

# Inicializacion de extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

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
    
    # ------------------ JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    # Usaremos cookies HttpOnly para SSR sin JS
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False      # True en producción con HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Mínimo: desactiva CSRF; en prod actívalo

    jwt.init_app(app)

    @app.before_request
    def load_current_user():
        g.current_user_id = None
        try:
            verify_jwt_in_request(optional=True)
            g.current_user_id = get_jwt_identity()
        except Exception:
            pass

    @app.context_processor
    def inject_user():
        return {"current_user_id": getattr(g, "current_user_id", None)}

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
        from app.models import PostComment
        post = Posts.query.get_or_404(id)
        post_comments = db.session.query(PostComment).filter_by(post_id=post.post_id).all()
        return render_template('post.html', post=post, post_comments=post_comments)

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

    # ------------------ Endpoint Routing & Blueprints
    from app.routes.users_routes import UserRoutes
    UserRoutes(app)
    
    from app.routes.posts_routes import PostRoutes
    PostRoutes(app)
    
    from app.routes.post_vote_routes import PostVoteRoutes
    PostVoteRoutes(app)
    
    from app.routes.post_comment_routes import PostCommentRoutes
    PostCommentRoutes(app)

    from app.routes.auth_routes import AuthRoutes
    AuthRoutes(app)

    # ------------------

    return app

