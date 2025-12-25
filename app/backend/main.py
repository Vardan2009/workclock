import copy
import datetime
import os

from auth import generate_token, require_auth, validate_username, validate_password
from db import TOKEN_TTL, tasks_db, tokens, users, running_instances
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
    username = data.get("username", "").strip()
    password = data.get("password", "")

    is_valid, error_msg = validate_username(username)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 409

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

    if username in running_instances and task_id in running_instances[username]:
        instance = running_instances[username][task_id]
        started_at = datetime.datetime.fromisoformat(instance["started_at"])
        elapsed_sec = int((datetime.datetime.utcnow() - started_at).total_seconds())

        task = user_tasks[task_id]
        new_instance = {
            "id": len(task["task_instances"]) + 1,
            "est_duration_sec": instance["est_duration_sec"],
            "real_duration_sec": elapsed_sec,
            "timestamp_started": instance["started_at"],
        }
        task["task_instances"].append(new_instance)
        
        del running_instances[username][task_id]

    del user_tasks[task_id]
    return jsonify({"message": "Task deleted"})


@app.route("/tasks/<int:task_id>/instances/start", methods=["POST"])
@require_auth
def start_task_instance(task_id):
    data = request.json or {}
    username = request.user
    user_tasks = tasks_db.get(username, {})
    task = user_tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if username not in running_instances:
        running_instances[username] = {}

    running_instances[username][task_id] = {
        "est_duration_sec": data.get("est_duration_sec", 0),
        "started_at": datetime.datetime.utcnow().isoformat(),
    }

    return jsonify({
        "task_id": task_id,
        "est_duration_sec": data.get("est_duration_sec", 0),
        "started_at": running_instances[username][task_id]["started_at"],
    }), 201


@app.route("/tasks/<int:task_id>/instances/elapsed", methods=["GET"])
@require_auth
def get_elapsed_time(task_id):
    username = request.user
    
    if username not in running_instances or task_id not in running_instances[username]:
        return jsonify({"error": "No running instance"}), 404

    instance = running_instances[username][task_id]
    started_at = datetime.datetime.fromisoformat(instance["started_at"])
    elapsed_sec = int((datetime.datetime.utcnow() - started_at).total_seconds())

    return jsonify({
        "task_id": task_id,
        "elapsed_sec": elapsed_sec,
        "est_duration_sec": instance["est_duration_sec"],
    })


@app.route("/tasks/<int:task_id>/instances/stop", methods=["POST"])
@require_auth
def stop_task_instance(task_id):
    username = request.user
    user_tasks = tasks_db.get(username, {})
    task = user_tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if username not in running_instances or task_id not in running_instances[username]:
        return jsonify({"error": "No running instance"}), 404

    instance = running_instances[username][task_id]
    started_at = datetime.datetime.fromisoformat(instance["started_at"])
    elapsed_sec = int((datetime.datetime.utcnow() - started_at).total_seconds())

    new_instance = {
        "id": len(task["task_instances"]) + 1,
        "est_duration_sec": instance["est_duration_sec"],
        "real_duration_sec": elapsed_sec,
        "timestamp_started": instance["started_at"],
    }

    task["task_instances"].append(new_instance)
    del running_instances[username][task_id]

    return jsonify(new_instance), 201


if __name__ == "__main__":
    app.run(debug=True)