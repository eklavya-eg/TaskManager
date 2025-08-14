from ..extensions import db
from ..models.users import User
from ..utils import detach
from werkzeug.security import generate_password_hash, check_password_hash

def SignUp(name:str, userid:str, password:str):
    exists = (
        db.session.query(User.userid).filter(User.userid==userid).first()
    )
    if exists: return None, 409
    pass_hash = generate_password_hash(password=password)
    user = User(userid=userid, password=pass_hash, name=name)
    db.session.add(user)
    db.session.commit()
    user = detach(user)
    return user, 200

def SignIn(userid:str, password:str):
    user = (
        db.session.query(User.id, User.userid, User.password).filter(User.userid==userid).first()
    )
    if(user==None):
        return None, 404, False
    user = {
        "id": str(user.id),
        "userid": user.userid,
        "password": user.password
    }
    verify = check_password_hash(user.get("password"), password)
    return user, 200 if verify else 401, verify