from flask import request, jsonify, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.models.posts_entity import db, Posts
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import posts_service
from app.services.posts_service import PostsService

def PostRoutes(app):
    @app.route('/api/posts', methods=['GET', 'POST'])
    @jwt_required(optional=True)
    def post_api():
        if request.method == 'GET':
            try:
                current_user_id = get_jwt_identity()
                
                posts_service = PostsService()
                all_posts = posts_service.get_all()

                post_list = [
                    {
                        "post_id": post.post_id,
                        "created_by": post.created_by,
                        "creator" : post.creator.username,
                        "title": post.title,
                        "commentary": post.commentary,
                        "affected_area": post.affected_area,
                        "priority": post.priority,
                        "creation_date": post.creation_date.isoformat(),
                        "expiration_date": post.expiration_date.isoformat(),
                        
                        "is_mine": post.created_by == current_user_id,
                    } for post in all_posts
                ]

                return jsonify(post_list), 200

            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        elif request.method == 'POST':
            try:
                print("Received form data:", request.form)

                if request.is_json:
                    data = request.get_json()
                else:
                    data = request.form

                title = data.get('title')
                commentary = data.get('commentary')
                affected_area = data.get('affected_area')
                priority = data.get('priority')
                expiration_date = data.get('expiration_date')
                created_by = get_jwt_identity()
                
                print("Created by:" + created_by)

                if not all([title, commentary, priority]):
                    return jsonify({"error": "Missing one or more required fields"}), 400

                new_post = Posts(
                    title=title,
                    commentary=commentary,
                    affected_area=affected_area,
                    priority=priority,
                    expiration_date=expiration_date,
                    created_by=created_by
                )
            
                db.session.add(new_post)
                db.session.commit()

                return redirect(url_for('post', id=new_post.post_id))

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": f"Database integrity error: {str(e.orig)}"}), 400

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None

    # Delete hardcodeado para no usar javascript jeje
    @app.route("/api/post/<int:post_id>", methods=["POST"])
    @jwt_required(optional=True)
    def delete_post(post_id):
        if request.form.get("_method") == "DELETE":
            from app.models.posts_entity import Posts
            post = Posts.query.get_or_404(post_id)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('home'))
        return None