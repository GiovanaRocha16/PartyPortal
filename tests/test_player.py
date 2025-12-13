import os
import pytest
import tempfile
from app.models.player import Player
from app.models.user import User
from app.models.database import Database

@pytest.fixture(autouse=True)
def setup():
    """
    Configura banco limpo em arquivo temporário para cada teste.
    Player e User compartilham o mesmo Database.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db = Database(path=path)

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    Player.db = db
    User.db = db

    yield

    os.remove(path)


def test_create_for_user():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    p = Player.create_for_user(u.id)

    assert p is not None
    assert p.user_id == u.id
    assert p.score == 0


def test_get_by_user():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    p = Player.create_for_user(u.id)

    fetched = Player.get_by_user(u.id)

    assert fetched is not None
    assert fetched.id == p.id


def test_add_score():
    u = User(username="gih", password="123", is_admin=0)
    u.save()
    p = Player.create_for_user(u.id)

    p.add_score(10)
    updated = Player.get_by_user(u.id)

    assert updated.score == 10


def test_delete_by_user_id():
    u = User(username="gih", password="123", is_admin=0)
    u.save()

    Player.create_for_user(u.id)
    Player.delete_by_user_id(u.id)

    assert Player.get_by_user(u.id) is None
