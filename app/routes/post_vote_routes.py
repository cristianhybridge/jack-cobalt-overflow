from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models.post_vote_entity import db, PostVote # We'll need to create this file

def PostVoteRoutes(app):
    """
    Defines the routes for handling post votes (likes).
    """
    # The API endpoint is now specific to votes.
    @app.route('/api/post-vote', methods=['GET', 'POST'])
    def post_vote():
        if request.method == 'GET':
            try:
                all_votes = PostVote.query.all()

                vote_list = [
                    {
                        "post_vote_id": vote.post_vote_id,
                        "post_id": vote.post_id,
                        "created_by": vote.created_by,
                        "vote": vote.vote,
                        "creation_date": vote.creation_date.isoformat()
                    }
                    for vote in all_votes
                ]
                return jsonify(vote_list), 200
            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        elif request.method == 'POST':
            try:
                if not request.is_json:
                    return jsonify({"error": "Request must be JSON"}), 400

                data = request.get_json()

                post_id = data.get("post_id")
                created_by = data.get("created_by")
                vote_value = data.get("vote", True)

                if not post_id or not created_by:
                    return jsonify({"error": "Missing required fields (post_id, created_by)."}), 400

                new_vote = PostVote(
                    post_id=post_id,
                    created_by=created_by,
                    vote=vote_value
                )

                db.session.add(new_vote)
                db.session.commit()

                return jsonify({"message": "Vote recorded successfully!", "vote_id": new_vote.post_vote_id}), 201

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": f"Database integrity error: {str(e.orig)}. A user can only vote once per post."}), 409

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None

