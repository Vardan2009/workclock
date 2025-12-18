import copy
import datetime
import os

from auth import generate_token, require_auth
from db import TOKEN_TTL, tasks_db, tokens, users
from flask import Flask, jsonify, request
from flask_cors import CORS
from passhash import hash_password, verify_password

app = Flask(__name__)

ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173",  # local dev default
)

CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS.split(",")}})


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

    return user_data


@app.route("/logout", methods=["POST"])
@require_auth
def logout():
    auth = request.headers.get("Authorization")
    token = auth.replace("Bearer ", "")
    tokens.pop(token, None)
    return jsonify({"message": "Logged out"})


@app.route("/tasks", methods=["GET"])
@require_auth
def get_tasks():
    username = request.user
    user_tasks = tasks_db.get(username, {})
    return jsonify({"tasks": list(user_tasks.values())})


@app.route("/tasks", methods=["POST"])
@require_auth
def create_task():
    data = request.json or {}
    username = request.user
    title = data.get("title")
    icon = data.get("icon", "📝")

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    if username not in tasks_db:
        tasks_db[username] = {}

    task_id = len(tasks_db[username]) + 1
    task = {
        "id": task_id,
        "title": title,
        "icon": icon,
        "task_instances": [],
        "task_note": "",
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    tasks_db[username][task_id] = task
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>/note", methods=["PATCH"])
@require_auth
def update_task_note(task_id):
    username = request.user
    user_tasks = tasks_db.get(username, {})
    task = user_tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    
    if not data or "note" not in data:
        return jsonify({"error": "Missing note"}), 400

    task["task_note"] = data["note"]

    return jsonify({"message": "Note updated", "task": task}), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
@require_auth
def get_task(task_id):
    username = request.user
    user_tasks = tasks_db.get(username, {})
    task = user_tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@require_auth
def delete_task(task_id):
    username = request.user
    user_tasks = tasks_db.get(username, {})

    if task_id not in user_tasks:
        return jsonify({"error": "Task not found"}), 404

    del user_tasks[task_id]
    return jsonify({"message": "Task deleted"})


@app.route("/tasks/<int:task_id>/instances", methods=["POST"])
@require_auth
def add_task_instance(task_id):
    data = request.json or {}
    username = request.user
    user_tasks = tasks_db.get(username, {})
    task = user_tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    instance = {
        "id": len(task["task_instances"]) + 1,
        "est_duration_sec": data.get("est_duration_sec", 0),
        "real_duration_sec": data.get("real_duration_sec", 0),
        "timestamp_started": data.get("timestamp_started"),
    }

    task["task_instances"].append(instance)
    return jsonify(instance), 201


if __name__ == "__main__":
    app.run(debug=True)
