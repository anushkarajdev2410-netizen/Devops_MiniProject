import pytest
from app import create_app

@pytest.fixture()
def app(tmp_path):
    db_file = tmp_path / "test.db"
    application = create_app({"TESTING": True, "DATABASE": str(db_file)})
    yield application

@pytest.fixture()
def client(app):
    return app.test_client()
