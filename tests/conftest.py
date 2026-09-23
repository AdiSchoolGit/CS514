import pytest

import db


@pytest.fixture
def conn(tmp_path):
    path = tmp_path / "test.db"
    db.init_db(path)
    conn = db.connect(path)
    yield conn
    conn.close()
