from .extensions import db
from datetime import datetime, timezone, timedelta
import jwt

STATUS_CODES = {
    200: "Success",
    400: "Wrong inputs",
    401: "Wrong password",
    403: "Not authorized",
    404: "Resource not found",
    409: "Resource already exists",
    500: "Internal server error"
}

def detach(obj):
    if not obj: return None
    if(isinstance(obj, list)):
        obj_list = []
        for item in obj:
            # db.session.expunge(item)
            obj_list.append({c.name:getattr(item, c.name) for c in item.__table__.columns})
        return obj_list
    else:
        # db.session.expunge(obj)
        return {c.name:getattr(obj, c.name) for c in obj.__table__.columns}

def jwtEncode(payload:dict, JWT_SECRET:str):
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)
    auth = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return auth

def jwtDecode(token:str, JWT_SECRET:str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return payload
