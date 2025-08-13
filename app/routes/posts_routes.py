from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models.posts_entity import db, Posts

def PostRoutes(app):
    @app.route('/api/posts', methods=['GET', 'POST'])
    def post_api():
        if request.method == 'GET':
            try:
                all_posts = Posts.query.all()

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
                        "expiration_date": post.expiration_date.isoformat()
                    } for post in all_posts
                ]

                return jsonify(post_list), 200

            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        elif request.method == 'POST':
            try:
                if not request.is_json:
                    return jsonify({"error": "Request must be JSON"}), 400

                data = request.get_json()

                title = data.get('title')
                commentary = data.get('commentary')
                affected_area = data.get('affected_area')
                priority = data.get('priority')
                created_by = data.get('created_by')

                if not all([title, commentary, affected_area, priority, created_by]):
                    return jsonify({"error": "Missing one or more required fields"}), 400

                new_post = Posts(
                    title=title,
                    commentary=commentary,
                    affected_area=affected_area,
                    priority=priority,
                    created_by=created_by
                )

                db.session.add(new_post)
                db.session.commit()

                return jsonify({"message": "Post created successfully!", "post_id": new_post.post_id}), 201

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": f"Database integrity error: {str(e.orig)}"}), 400

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None