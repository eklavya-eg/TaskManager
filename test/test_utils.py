import pytest
from app.utils import detach, jwtEncode, jwtDecode

def test_detach_single_object():
    class Dummy:
        def __init__(self):
            self.id = 1
            self.name = "Alice"
        __table__ = type("table", (), {"columns": [type("col", (), {"name": "id"}), type("col", (), {"name": "name"})]})()
    obj = Dummy()
    result = detach(obj)
    assert result["id"] == 1
    assert result["name"] == "Alice"

def test_detach_list_of_objects():
    class Dummy:
        def __init__(self, i):
            self.id = i
            self.name = f"Name{i}"
        __table__ = type("table", (), {"columns": [type("col", (), {"name": "id"}), type("col", (), {"name": "name"})]})()
    objs = [Dummy(1), Dummy(2)]
    result = detach(objs)
    assert result[0]["id"] == 1
    assert result[1]["name"] == "Name2"

def test_jwt_encode_decode():
    payload = {"id": "123"}
    secret = "testsecret"
    token = jwtEncode(payload.copy(), secret)
    decoded = jwtDecode(token, secret)
    assert decoded["id"] == "123"
