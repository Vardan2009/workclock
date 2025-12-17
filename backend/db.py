import datetime

users = {}  # username -> {password_hash, other user data}
tokens = {}  # token -> {username, expires_at}

TOKEN_TTL = datetime.timedelta(hours=10)
