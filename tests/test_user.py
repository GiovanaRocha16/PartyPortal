import os
import pytest
import tempfile
from app.models.user import User
from app.models.database import Database

@pytest.fixture(autouse=True)
def clean_database():
    """Cria um banco temporário limpo para cada teste com a tabela 'users'."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    User.db = Database(path)
    User.db.initialize_database()

    User.db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)

    yield

    os.remove(path)


def test_user_create_and_get():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    fetched = User.get_by_username("gih")

    assert fetched is not None
    assert fetched.username == "gih"
    assert fetched.password == "123"
    assert fetched.is_admin == 0


def test_user_exists():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    assert User.exists("gih") is True
    assert User.exists("nao_existe") is False


def test_authenticate():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    ok = User.authenticate("gih", "123")
    fail = User.authenticate("gih", "senha_errada")

    assert ok is not None
    assert fail is None


def test_set_admin():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    User.set_admin(u.id, True)

    updated = User.get_by_id(u.id)
    assert updated.is_admin == 1
