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
    expected = {
        "count": 1,
        "users": [
            {
                "email": "testuser@email.com",
                "joined_at_datetime": datetime.utcnow().strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                ),
            }
        ],
    }
    assert expected == json.loads(get_res.get_data(as_text=True))
