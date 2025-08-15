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
    """
    User Signup
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                min length: 1
                example: abcd
              userid:
                type: string
                min length: 1
                example: abcd
              password:
                type: string
                min length
                example: 12345678
            required:
              - name
              - userid
              - password
    responses:
      200:
        description: Successful signup
        content:
          application/json:
            example:
              message: Success
              id: "user_uuid_here"
              auth: "Bearer token_here"
      400:
        description: Wrong inputs
        content:
          application/json:
            example:
              message: Wrong inputs
      409:
        description: Resource already exists
        content:
          application/json:
            example:
              message: Resource already exists
    """
    data = request.get_json()
    try:
        v_data = SignUpSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400
    
    user, sc = UserServices.SignUp(v_data["name"], v_data["userid"], v_data["password"])

    if sc==200: return jsonify({
        "message": STATUS_CODES.get(sc),
        "id": str(user.get("id")),
        "auth": f'''{str(jwtEncode({"id":str(user.get("id"))}, JWT_SECRET))}'''}), sc

    return jsonify({"message": STATUS_CODES.get(sc)}), sc

@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    """
    User Signin
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              userid:
                type: string
                min length: 1
                example: abcd
              password:
                type: string
                min length: 8
                example: secret123
            required:
              - userid
              - password
    responses:
      200:
        description: Successful signin
        content:
          application/json:
            example:
              message: Success
              id: "user_uuid_here"
              auth: "Bearer token_here"
      400:
        description: Wrong inputs
        content:
          application/json:
            example:
              message: Wrong inputs
      401:
        description: Wrong password
        content:
          application/json:
            example:
              message: Wrong password
      404:
        description: User not found
        content:
          application/json:
            example:
              message: Resource not found
    """
    data = request.get_json()
    try:
        v_data = SignInSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400
    user, sc, verify = UserServices.SignIn(v_data["userid"], v_data["password"])

    if sc==200: return jsonify({
        "message": STATUS_CODES.get(sc),
        "id": str(user.get("id")),
        "auth": f'''{str(jwtEncode({"id":str(user.get("id"))}, JWT_SECRET))}'''}), sc
    
    return jsonify({"message": STATUS_CODES.get(sc), "user": user}), sc