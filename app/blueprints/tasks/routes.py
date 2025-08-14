from flask import jsonify, Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.dialects.postgresql import UUID
from ...services import tasks as TaskServices
from ...schemas.tasks import *
from ...utils import *
from ...middlewares.auth import auth_middleware
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_blueprint.route("/", methods=["GET"])
@auth_middleware
def tasks():
    uuid = request.user_uuid
    if not uuid: return jsonify({"message": STATUS_CODES.get(403)}), 403
    try:
        tasks, sc = TaskServices.FetchTasks(userid=uuid)
    except Exception as e:
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    return jsonify({
        "message": STATUS_CODES.get(sc),
        "tasks": tasks
    }), sc


@tasks_blueprint.route("/<task_id>", methods=["GET"])
@auth_middleware
def task(task_id:str|UUID):
    user_uuid = request.user_uuid
    if (not user_uuid): return jsonify({"message": STATUS_CODES.get(403)}), 403
    if (not task_id): return jsonify({"message": STATUS_CODES.get(400)}), 400

    try:
        task, sc = TaskServices.FetchTask(task_id, user_uuid)
    except Exception as e:
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    
    return jsonify({
        "message": STATUS_CODES.get(sc),
        "tasks": task
    }), sc

@tasks_blueprint.route("/", methods=["POST"])
@auth_middleware
def create_tasks():
    user_uuid = request.user_uuid
    data = request.get_json()
    if (not user_uuid): return jsonify({"message": STATUS_CODES.get(403)}), 403

    try:
        v_data = CreateTaskSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400
    description = v_data.get("description")
    
    if not description: description = ""
    try:
        task, sc = TaskServices.CreateTask(v_data.get("title"), description, user_uuid)
    except Exception as e:
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    return jsonify({
        "message": STATUS_CODES.get(sc),
        "task": task
    }), sc

@tasks_blueprint.route("/<task_id>", methods=["PUT"])
@auth_middleware
def update_task(task_id:str|UUID):
    user_uuid = request.user_uuid
    data = request.get_json()
    if (not user_uuid): return jsonify({"message": STATUS_CODES.get(403)}), 403
    if (not task_id): return jsonify({"message": STATUS_CODES.get(400)}), 400

    try:
        v_data = UpdateTaskSchema().load(data)
    except ValidationError as e:
        return jsonify({"message": STATUS_CODES.get(400)}), 400

    try:
        task, sc = TaskServices.UpdateTask(task_id, user_uuid, v_data.get("title"), v_data.get("description"), v_data.get("completed"))
    except Exception as e:
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    return jsonify({
        "message": STATUS_CODES.get(sc),
        "task": task
    }), sc

@tasks_blueprint.route("/<task_id>", methods=["DELETE"])
@auth_middleware
def delete_task(task_id:str|UUID):
    user_uuid = request.user_uuid
    if (not user_uuid): return jsonify({"message": STATUS_CODES.get(403)}), 403
    if (not task_id): return jsonify({"message": STATUS_CODES.get(400)}), 400
    
    try:
        deleted, sc = TaskServices.DeleteTask(task_id, user_uuid)
    except Exception as e:
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    return jsonify({
        "message": STATUS_CODES.get(sc),
    }), sc
