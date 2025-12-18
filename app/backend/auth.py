import datetime
import secrets

from db import tokens
from flask import Flask, jsonify, request


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_user_from_token(token: str):
    data = tokens.get(token)
    if not data:
        return None

    if data["expires_at"] < datetime.datetime.utcnow():
        del tokens[token]
        return None

    return data["username"]


def require_auth(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth.replace("Bearer ", "")
        username = get_user_from_token(token)

        if not username:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user = username
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
