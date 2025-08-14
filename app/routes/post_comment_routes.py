from flask import request, jsonify, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.models.post_comment_entity import db, PostComment
from flask_jwt_extended import jwt_required, get_jwt_identity


def PostCommentRoutes(app):
    @app.route('/api/post-comment', methods=['GET', 'POST'])
    @jwt_required(optional=True)
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
                print("Received form data:", request.form)

                # Check if it's form data or JSON
                if request.is_json:
                    data = request.get_json()
                else:
                    data = request.form

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

                return redirect(url_for('post', id=post_id))

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": f"Database integrity error: {str(e.orig)}"}), 400

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None
    @app.route('/api/post-comment/<int:id>', methods=['DELETE'])
    @jwt_required(optional=True)
    def delete_post_comment(id):
        try:
            comment_to_delete = PostComment.query.get_or_404(id)

            db.session.delete(comment_to_delete)
            db.session.commit()

            return jsonify({"message": f"Comment {id} deleted successfully."}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    # Delete hardcodeado para no usar javascript jeje
    @app.route("/api/post-comment/<int:comment_id>", methods=["POST"])
    @jwt_required(optional=True)
    def delete_comment(comment_id):
        if request.form.get("_method") == "DELETE":
            comment = PostComment.query.get_or_404(comment_id)
            post_id = comment.post_id
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('post', id=post_id))
        return None