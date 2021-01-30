import pytest

from src import app as flask_app
from src.app import db as flask_db
from src.app import UsersModel


@pytest.fixture
def db():
    yield flask_db


@pytest.fixture
def app(db):
    yield flask_app
    db.session.query(UsersModel).delete()


@pytest.fixture
def client(app):
    return app.test_client()
