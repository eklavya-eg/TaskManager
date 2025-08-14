from flask import jsonify, Blueprint, request
from marshmallow import ValidationError
from ...services import users as UserServices
from ...schemas.auth import *
from ...utils import *
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        v_data = SignUpSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400
    
    user, sc = UserServices.SignUp(v_data["name"], v_data["userid"], v_data["password"])

    if sc==200: return jsonify({
        "message": STATUS_CODES.get(sc),
        "id": str(user.get("id")),
        "auth": f'''Bearer {str(jwtEncode({"id":str(user.get("id"))}, JWT_SECRET))}'''}), sc

    return jsonify({"message": STATUS_CODES.get(sc)}), sc

@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    try:
        v_data = SignInSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400
    user, sc, verify = UserServices.SignIn(v_data["userid"], v_data["password"])

    if sc==200: return jsonify({
        "message": STATUS_CODES.get(sc),
        "id": str(user.get("id")),
        "auth": f'''Bearer {str(jwtEncode({"id":str(user.get("id"))}, JWT_SECRET))}'''}), sc
    
    return jsonify({"message": STATUS_CODES.get(sc), "user": user}), sc