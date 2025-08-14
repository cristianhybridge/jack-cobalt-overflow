from flask import render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
from app.services.users_service import UsersService
from app.repositories.base_repository import UsersRepository

users_service = UsersService(UsersRepository())

def AuthRoutes(app):
    @app.get("/login")
    def login_view():
        return render_template("login.html")

    @app.post("/login")
    def login_post():
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_service.verify_credentials(username, password)
        if not user:
            flash("Usuario o contraseña inválidos", "danger")
            return redirect(url_for("login_view"))

        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=6))
        resp = make_response(redirect(url_for("home")))  # ajusta a tu home
        set_access_cookies(resp, access_token)
        return resp

    @app.post("/logout")
    def logout():
        resp = make_response(redirect(url_for("home")))  # ajusta a tu home
        unset_jwt_cookies(resp)
        return resp
