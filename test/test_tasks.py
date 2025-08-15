import json
from app import app_ as app

app=app()

def get_auth_token():
    client = app.test_client()
    client.post("/auth/signup", data=json.dumps({
        "name": "task test",
        "userid": "taskuser",
        "password": "12345678"
    }), content_type="application/json")

    response = client.post("/auth/signin", data=json.dumps({
        "userid": "taskuser",
        "password": "12345678"
    }), content_type="application/json")
    return response.get_json()["auth"]

def test_create_task():
    client = app.test_client()
    auth = get_auth_token()
    payload = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks", data=json.dumps(payload),
                           headers={"auth": f"Bearer {auth}"},
                           content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "task" in data

def test_get_tasks():
    client = app.test_client()
    auth = get_auth_token()
    response = client.get("/tasks",
                          headers={"auth": f"Bearer {auth}"})
    assert response.status_code == 200
    assert isinstance(response.get_json().get("tasks"), list)

def test_get_unique_task():
    client = app.test_client()
    auth = get_auth_token()

    response = client.get("/tasks",
                          headers={"auth": f"Bearer {auth}"})
    taskid = response.get_json().get("tasks")[0].get("id")
    
    response = client.get(f"/tasks/{taskid}",
                          headers={"auth": f"Bearer {auth}"})
    assert response.status_code == 200
    assert isinstance(response.get_json().get("task"), dict)

def test_update_task():
    client = app.test_client()
    auth = get_auth_token()

    response = client.get("/tasks",
                          headers={"auth": f"Bearer {auth}"})
    taskid = response.get_json().get("tasks")[0].get("id")
    task_completed = response.get_json().get("tasks")[0].get("completed")
    task_title = response.get_json().get("tasks")[0].get("title")
    task_updated_at = response.get_json().get("tasks")[0].get("updated_at")
    payload = {
        "title": "Change",
        "completed": True
    }
    print(response.get_json())
    response = client.put(f"/tasks/{taskid}",
                          data=json.dumps(payload),
                          headers={"auth": f"Bearer {auth}"},
                          content_type="application/json")
    print(response.get_json())
    assert response.status_code == 200
    task = response.get_json().get("task")
    assert task_completed!=response.get_json().get("task").get("completed")
    assert task_updated_at!=response.get_json().get("task").get("updated_at")
    assert response.get_json().get("task").get("title")=="Change"
    assert task_title!=response.get_json().get("task").get("title")
    assert isinstance(response.get_json().get("task"), dict)

def test_update_task():
    client = app.test_client()
    auth = get_auth_token()

    response = client.get("/tasks",
                          headers={"auth": f"Bearer {auth}"})
    taskid = response.get_json().get("tasks")[0].get("id")
    print(response.get_json())
    response = client.delete(f"/tasks/{taskid}",
                          headers={"auth": f"Bearer {auth}"})
    print(response.get_json())
    assert response.status_code == 200