from flask import request, render_template, redirect, url_for, flash
from psycopg2.errors import UniqueViolation

from app.models.users_entity import db, Users
from sqlalchemy.exc import IntegrityError

def register_users_routes(app):
    @app.route('/api/users', methods=['GET', 'POST'])
    def users():
        if request.method == 'GET':
            all_users = Users.query.all()
            users_list = [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "nickname": user.nickname,
                }
                for user in all_users
            ]
            return render_template('users.html', users=users_list)

        else:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form

            new_user = Users(
                username=data.get("username"),
                password=data.get("password"),
                nickname=data.get("nickname")
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('home'))
            except IntegrityError as e:
                db.session.rollback()
                # Check if the original exception is UniqueViolation
                if isinstance(e.orig, UniqueViolation):
                    flash("Username or nickname already exists.", "danger")
                    
                    return render_template(
                        'register.html',
                        username=data.get("username"),
                        nickname=data.get("nickname")), 409
                
                else:
                    flash("Database error occurred.", "danger")

                    return render_template(
                        'register.html',
                        username=data.get("username"),
                        nickname=data.get("nickname")), 500