import os
import pytest
import tempfile
from app.models.model import Model
from app.models.database import Database

@pytest.fixture(autouse=True)
def clean_database():
    """Recria o banco limpo antes de cada teste usando arquivo temporário."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    Model.db = Database(path=path)

    Model.db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    """)

    yield

    os.remove(path)


def test_model_insert_and_get():
    class Temp(Model):
        table = "users"
        fields = ["id", "username", "password", "is_admin"]

    u = Temp(username="gih", password="123", is_admin=0)
    u.save()

    row = Model.db.fetch_one("SELECT id FROM users WHERE username=?", ("gih",))
    user_id = row[0]

    fetched = Temp.get(user_id)

    assert fetched is not None
    assert fetched.username == "gih"
    assert fetched.password == "123"
    assert fetched.is_admin == 0


def test_model_update():
    class Temp(Model):
        table = "users"
        fields = ["id", "username", "password", "is_admin"]

    u = Temp(username="gih", password="123", is_admin=0)
    u.save()

    row = Model.db.fetch_one("SELECT id FROM users WHERE username=?", ("gih",))
    user_id = row[0]

    Temp.update(user_id, username="novo")

    updated = Temp.get(user_id)
    assert updated.username == "novo"


def test_model_delete():
    class Temp(Model):
        table = "users"
        fields = ["id", "username", "password", "is_admin"]

    u = Temp(username="gih", password="123", is_admin=0)
    u.save()

    row = Model.db.fetch_one("SELECT id FROM users WHERE username=?", ("gih",))
    user_id = row[0]

    u.id = user_id
    u.delete()

    assert Temp.get(user_id) is None
