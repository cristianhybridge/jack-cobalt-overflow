from flask import redirect, url_for, jsonify, Blueprint, request, render_template
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from werkzeug.security import check_password_hash
from datetime import timedelta

from app.services.users_service import UsersService
from app.repositories.base_repository import UsersRepository

auth_bp = Blueprint("auth", __name__)
users_service = UsersService(UsersRepository())

def AuthRoutes(app):

    # ------------------ REGISTER ------------------
    @auth_bp.route('/api/register', methods=['POST'])
    def register():

        print("Received form data:", request.form)

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        username = data.get('username')
        password = data.get('password')
        nickname = data.get('nickname')

        if not username or not password or not nickname:
            return jsonify({"success": False, "message": "Faltan campos requeridos"}), 400

        existing_user = users_service.find_user_by_username(username)
        if existing_user:
            return jsonify({"success": False, "message": "El nombre de usuario ya existe"}), 409

        new_user = users_service.create_user(username, password, nickname)

        result = jsonify({
            "success": True,
            "message": f"Usuario {new_user.username} creado exitosamente!",
            "user_id": new_user.user_id
        }), 201
        
        print(result)

        return redirect(url_for('home'))

    # ------------------ LOGIN ------------------
    @app.post("/api/login")
    def api_login():
        from app.models.users_entity import Users
        data = request.get_json() if request.is_json else request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            # If HTML form, render template with error
            if not request.is_json:
                return render_template("login.html", error="Ingresa un usuario y contraseña.")
            return jsonify({"error": "Ingresa un usuario y contraseña."}), 400

        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            if not request.is_json:
                return render_template("login.html", error="Usuario o contraseña incorrectos.")
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

        # JWT valido por 1 dia
        access_token = create_access_token(
            identity=str(user.user_id),
            expires_delta=timedelta(days=1)
        )

        # Una vez logueado, redirecciona al home con las cookies del JWT para permanecer con la sesion iniciada
        resp = redirect(url_for("home"))
        set_access_cookies(resp, access_token)
        return resp

    # ------------------ LOGOUT ------------------
    @app.post("/api/logout")
    def api_logout():
        resp = redirect(url_for("home"))
        unset_jwt_cookies(resp)
        return resp
