import json
import os
from datetime import datetime


def test_index(app, client):
    res = client.get("/")
    assert res.status_code == 200
    expected = {"hello": "world", "environment": os.environ["FLASK_ENV"]}
    assert expected == json.loads(res.get_data(as_text=True))


def test_users(app, client):
    post_res = client.post(
        "/users",
        data=json.dumps({"email": "testuser@email.com", "pw_hash": "f873jf83gj93j"}),
        headers={"Content-Type": "application/json"},
    )
    assert post_res.status_code == 201
    get_res = client.get("/users")
    assert get_res.status_code == 200
    res_data = json.loads(get_res.get_data(as_text=True))
    assert res_data["count"] == 1
    assert res_data["users"][0]["email"] == "testuser@email.com"
    assert res_data["users"][0]["joined_at_datetime"]  # check if it exists
