import copy
import datetime

from auth import generate_token, require_auth
from db import TOKEN_TTL, tokens, users
from flask import Flask, jsonify, request
from flask_cors import CORS
from passhash import hash_password, verify_password

app = Flask(__name__)

CORS(app)


@app.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = {"password_hash": hash_password(password), "username": username}

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token()
    tokens[token] = {
        "username": username,
        "expires_at": datetime.datetime.utcnow() + TOKEN_TTL,
    }

    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": int(TOKEN_TTL.total_seconds()),
        }
    )


@app.route("/user", methods=["GET"])
@require_auth
def user():
    user_data = copy.copy(users[request.user])

    del user_data["password_hash"]

    print(user_data)

    return user_data


@app.route("/logout", methods=["POST"])
@require_auth
def logout():
    auth = request.headers.get("Authorization")
    token = auth.replace("Bearer ", "")
    tokens.pop(token, None)
    return jsonify({"message": "Logged out"})


# --------------------
# Run
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
