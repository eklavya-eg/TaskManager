import json
import pytest
from app import app_ as app

app=app()

def test_signup_success():
    client = app.test_client()
    payload = {
        "name": "abcdtest",
        "userid": "abcd",
        "password": "12345678"
    }
    response = client.post("/auth/signup", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    assert "auth" in data

def test_signup_missing_field():
    client = app.test_client()
    payload = {
        "name": "abcdtest",
        "password": "12345678"
    }
    response = client.post("/auth/signup", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400

def test_signin_success():
    client = app.test_client()
    client.post("/auth/signup", data=json.dumps({
        "name": "logintest",
        "userid": "loginuser",
        "password": "12345678"
    }), content_type="application/json")

    payload = {
        "userid": "loginuser",
        "password": "12345678"
    }
    response = client.post("/auth/signin", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "auth" in data
    assert "id" in data
