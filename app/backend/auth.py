import datetime
import secrets
from functools import wraps
from flask import request, jsonify

from db import tokens

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 32
MIN_PASSWORD_LENGTH = 8
TOKEN_LENGTH = 32

def generate_token() -> str:
    return secrets.token_urlsafe(TOKEN_LENGTH)

def validate_username(username: str) -> tuple[bool, str]:
    if not username or not isinstance(username, str):
        return False, "Username must be a string"
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters"
    if len(username) > MAX_USERNAME_LENGTH:
        return False, f"Username must be at most {MAX_USERNAME_LENGTH} characters"
    if not username.isalnum() and "_" not in username:
        return False, "Username can only contain alphanumeric characters and underscores"
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    if not password or not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
    return True, ""

def get_user_from_token(token: str) -> str | None:
    if not token or not isinstance(token, str):
        return None
    
    data = tokens.get(token)
    if not data:
        return None

    if data["expires_at"] < datetime.datetime.utcnow():
        tokens.pop(token, None) 
        return None

    return data["username"]

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "").strip()
        
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth[7:] 
        
        if not token:
            return jsonify({"error": "Empty token"}), 401
        
        username = get_user_from_token(token)

        if not username:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user = username
        request.token = token 
        return f(*args, **kwargs)

    return wrapper