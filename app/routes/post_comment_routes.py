from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models.post_comment_entity import db, PostComment

def PostCommentRoutes(app):
    @app.route('/api/post-comment', methods=['GET', 'POST'])
    def post_comment():
        if request.method == 'GET':
            try:
                all_comments = PostComment.query.all()
                
                comment_list = [
                    {
                        "post_comment_id": comment.post_comment_id,
                        "post_id": comment.post_id,
                        "commentary": comment.commentary,
                        "created_by": comment.created_by,
                        
                        "creation_date": comment.creation_date.isoformat()
                    }
                    for comment in all_comments
                ]
                return jsonify(comment_list), 200
            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        elif request.method == 'POST':
            try:
                if not request.is_json:
                    return jsonify({"error": "Request must be JSON"}), 400

                data = request.get_json()

                post_id = data.get("post_id")
                created_by = data.get("created_by")
                commentary = data.get("commentary")

                if not post_id or not created_by or commentary is None:
                    return jsonify({"error": "Missing required fields (post_id, created_by, commentary)."}), 400

                new_comment = PostComment(
                    post_id=post_id,
                    commentary=commentary,
                    created_by=created_by
                )

                db.session.add(new_comment)
                db.session.commit()

                return jsonify({"message": "Comment created successfully!", "comment_id": new_comment.post_comment_id}), 201

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": f"Database integrity error: {str(e.orig)}"}), 400

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None