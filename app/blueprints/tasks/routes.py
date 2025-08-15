from flask import jsonify, Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.dialects.postgresql import UUID
from ...services import tasks as TaskServices
from ...schemas.tasks import *
from ...utils import *
from ...middlewares.auth import auth_middleware
from dotenv import load_dotenv
import traceback
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_blueprint.route("", methods=["GET"])
@auth_middleware
def tasks():
    """
    Get All Tasks
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of tasks
        content:
          application/json:
            example:
              message: Success
              tasks:
                - id: "task_uuid"
                  title: "Task 1"
                  description: "Description"
                  completed: false
      403:
        description: Not authorized
        content:
          application/json:
            example:
              message: Not authorized
      500:
        description: Internal server error
    """
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
    """
    Get Single Task by ID
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        schema:
          type: string
        description: Task UUID
    security:
      - BearerAuth: []
    responses:
      200:
        description: Task retrieved
        content:
          application/json:
            example:
              message: Success
              tasks:
                id: "task_uuid"
                title: "Task 1"
                description: "Description"
                completed: false
      400:
        description: Wrong inputs
      403:
        description: Not authorized
      404:
        description: Resource not found
      500:
        description: Internal server error
    """
    user_uuid = request.user_uuid
    if (not user_uuid): return jsonify({"message": STATUS_CODES.get(403)}), 403
    if (not task_id): return jsonify({"message": STATUS_CODES.get(400)}), 400

    try:
        task, sc = TaskServices.FetchTask(task_id, user_uuid)
    except Exception as e:
        traceback.print_exc()
        print(f"ERROR: {e}")  
        return jsonify({"message": STATUS_CODES.get(500)}), 500
    
    return jsonify({
        "message": STATUS_CODES.get(sc),
        "task": task
    }), sc

@tasks_blueprint.route("", methods=["POST"])
@auth_middleware
def create_tasks():
    """
    Create a New Task
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                example: New Task
              description:
                type: string
                example: Task description
            required:
              - title
    responses:
      200:
        description: Task created successfully
        content:
          application/json:
            example:
              message: Success
              task:
                id: "task_uuid"
                title: "New Task"
                description: "Task description"
                completed: false
      400:
        description: Wrong inputs
      403:
        description: Not authorized
      500:
        description: Internal server error
    """
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
    """
    Update a Task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        schema:
          type: string
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                example: Updated Task
              description:
                type: string
                example: Updated description
              completed:
                type: boolean
                example: true
    responses:
      200:
        description: Task updated successfully
      400:
        description: Wrong inputs
      403:
        description: Not authorized
      404:
        description: Resource not found
      500:
        description: Internal server error
    """
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
    """
    Delete a Task
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        schema:
          type: string
    security:
      - BearerAuth: []
    responses:
      200:
        description: Task deleted successfully
      400:
        description: Wrong inputs
      403:
        description: Not authorized
      404:
        description: Resource not found
      500:
        description: Internal server error
    """
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
