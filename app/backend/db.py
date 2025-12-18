import datetime

users = {}  # username -> {password_hash, other user data}
tokens = {}  # token -> {username, expires_at}
tasks_db = {}  # username -> {task_id -> task_data}

TOKEN_TTL = datetime.timedelta(hours=10)
