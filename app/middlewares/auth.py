from functools import wraps
from flask import request, jsonify
import jwt
import os
from ..utils import STATUS_CODES, jwtDecode
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def auth_middleware(f):
    @wraps(f)
    def auth(*args, **kwargs):
        auth_header = request.headers.get("auth")
        if not auth_header:
            return jsonify({"message": STATUS_CODES.get(403)}), 403
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        try:
            payload = jwtDecode(token, JWT_SECRET)
        except Exception as e:
            print(e)
            return jsonify({"message": STATUS_CODES.get(403)}), 403
        # except jwt.ExpiredSignatureError:
        #     return jsonify({"message": STATUS_CODES.get(403)}), 403
        # except jwt.InvalidTokenError:
        #     return jsonify({"message": STATUS_CODES.get(403)}), 403
        request.user_uuid = payload.get("id")
        return f(*args, **kwargs)
    return auth
