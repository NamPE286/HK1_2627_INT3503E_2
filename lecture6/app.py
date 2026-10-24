from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
import bcrypt
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "dev-secret-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

auth = HTTPBasicAuth()
jwt = JWTManager(app)

# hash password luc khoi tao
_users = {
    "an@vnu.edu.vn": {
        "pw": bcrypt.hashpw(b"correct horse battery staple", bcrypt.gensalt()),
        "role": "user",
    },
    "admin@vnu.edu.vn": {
        "pw": bcrypt.hashpw(b"adminpass123", bcrypt.gensalt()),
        "role": "admin",
    },
}


@auth.verify_password
def verify_password(username, password):
    if username not in _users:
        return False
    stored = _users[username]["pw"]
    pwd = password.encode() if isinstance(password, str) else password
    if bcrypt.checkpw(pwd, stored):
        return username
    return None


@auth.error_handler
def on_auth_error(status):
    return jsonify({"error": "unauthorized"}), 401, {
        "WWW-Authenticate": 'Basic realm="orders"'
    }


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role and claims.get("role") != "admin":
                return jsonify({"error": "forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/api/orders", methods=["GET"])
@auth.login_required
def list_orders_basic():
    return jsonify({
        "orders": ["o-001", "o-002"],
        "principal": auth.current_user()
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "missing credentials"}), 400

    user = _users.get(username)
    if not user:
        return jsonify({"error": "invalid"}), 401
    pwd = password.encode() if isinstance(password, str) else password
    if not bcrypt.checkpw(pwd, user["pw"]):
        return jsonify({"error": "invalid"}), 401

    additional = {"role": user["role"]}
    access = create_access_token(identity=username, additional_claims=additional)
    refresh = create_refresh_token(identity=username, additional_claims=additional)
    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    })


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    additional = {"role": claims.get("role", "user")}
    access = create_access_token(identity=identity, additional_claims=additional)
    return jsonify({"access_token": access})


@app.route("/api/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify({
        "user": get_jwt_identity(),
        "role": get_jwt().get("role")
    })


@app.route("/api/admin/stats", methods=["GET"])
@require_role("admin")
def admin_stats():
    return jsonify({"users": len(_users), "orders_today": 12})


@app.route("/api/orders-jwt", methods=["GET"])
@jwt_required()
def list_orders_jwt():
    return jsonify({
        "orders": ["o-001", "o-002"],
        "principal": get_jwt_identity()
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
