import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    database = tmp_path / "care.db"
    application = create_app(str(database))
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()

