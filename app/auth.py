# app/auth.py
from functools import wraps
from flask import request, abort, current_app

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            abort(401, description="Brak nagłówka Authorization")
        parts = auth_header.split()
        # spodziewamy się formatu: "Bearer <token>"
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            abort(401, description="Niepoprawny format nagłówka Authorization")
        token = parts[1]
        # weryfikujemy token
        if token != current_app.config['API_TOKEN']:
            abort(401, description="Nieprawidłowy token")
        return f(*args, **kwargs)
    return decorated
