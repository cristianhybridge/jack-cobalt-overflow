from flask import request, jsonify, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.models.users_entity import db, Users

def UserRoutes(app):
    @app.route('/api/users', methods=['GET', 'POST'])
    def handle_users():
        if request.method == 'GET':
            try:
                all_users = Users.query.all()
                users_list = [
                    {
                        "user_id": user.user_id,
                        "username": user.username,
                        "nickname": user.nickname,
                    }
                    for user in all_users
                ]

                return jsonify(users_list), 200

            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        elif request.method == 'POST':
            try:
                print("Received form data:", request.form)
                
                if request.is_json:
                    data = request.get_json()
                else:
                    data = request.form

                username = data.get("username")
                password = data.get("password")
                nickname = data.get("nickname")

                if not all([username, password, nickname]):
                    return jsonify({"error": "Missing one or more required fields"}), 400

                new_user = Users(
                    username=username,
                    password=password,
                    nickname=nickname
                )

                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for('home'))

            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": "Username or nickname already exists."}), 409

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        return None
