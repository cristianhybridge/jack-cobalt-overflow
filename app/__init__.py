from flask import Flask, render_template
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

from app.services.posts_service import PostsService
from app.models import Posts, PostComment

# Initialize extensions
from app.database import db
migrate = Migrate()
jwt = JWTManager()

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

    # ------------------ JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Use HttpOnly cookies
    app.config["JWT_COOKIE_SECURE"] = False         # True in production with HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False   # Enable in production

    jwt.init_app(app)

    # ------------------ Pages
    @app.route('/')
    def welcome():
        return render_template('welcome.html')
    
    @app.route('/home')
    def home():
        posts = PostsService().get_all()
        return render_template('home.html', posts=posts)

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/post/<int:id>')
    def post(id):
        post = Posts.query.get_or_404(id)
        post_comments = db.session.query(PostComment).filter_by(post_id=post.post_id).all()
        return render_template('post.html', post=post, post_comments=post_comments)

    @app.route('/post/new')
    def new_post():
        return render_template('new_post.html')

    @app.route('/profile/<int:id>')
    def profile(id):
        return render_template('profile.html', user_id=id)

    # --- Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Test DB connection
    try:
        from sqlalchemy import create_engine
        engine = create_engine(DATABASE_URL)
        with engine.connect():
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")

    # ------------------ Current User Injection
    def get_current_user():
        try:
            from app.models.users_entity import Users
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            print(f"DEBUG get_current_user(): user_id from JWT = {user_id}")
            if user_id:
                user = Users.query.get(user_id)
                print(f"DEBUG get_current_user(): loaded user = {user}")
                return user
        except Exception as e:
            print(f"DEBUG get_current_user(): error = {e}")
        return None

    @app.context_processor
    def inject_user():
        user = get_current_user()
        print("DEBUG inject_user():", {
            "jwt_identity": get_jwt_identity() if user else None,
            "user_obj": repr(user) if user else None
        })
        return dict(user=user, current_user_id=user.user_id if user else None)

    # ------------------ Endpoint Routing & Blueprints
    from app.routes.users_routes import UserRoutes
    UserRoutes(app)

    from app.routes.posts_routes import PostRoutes
    PostRoutes(app)

    from app.routes.post_vote_routes import PostVoteRoutes
    PostVoteRoutes(app)

    from app.routes.post_comment_routes import PostCommentRoutes
    PostCommentRoutes(app)

    from app.routes.auth_routes import AuthRoutes, auth_bp
    AuthRoutes(app)
    app.register_blueprint(auth_bp)

    return app
