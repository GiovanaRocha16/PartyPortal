import pytest
import tempfile
import os
from app.models.database import Database


@pytest.fixture
def db():
    """
    Cria um banco SQLite temporário em arquivo para cada teste.
    Garante que todas as conexões vejam o mesmo banco.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    database = Database(path=path)
    yield database

    os.remove(path)


def test_initialize_database(db):
    """Testa se as tabelas foram criadas corretamente."""
    con = db.connect()
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}

    assert "users" in tables
    assert "players" in tables
    assert "sessions" in tables

    con.close()


def test_execute_insert_and_fetch_one(db):
    """Testa INSERT e SELECT usando fetch_one."""
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("gih", "123", 0),
    )

    row = db.fetch_one(
        "SELECT username, password, is_admin FROM users WHERE username=?",
        ("gih",),
    )

    assert row is not None
    assert row[0] == "gih"
    assert row[1] == "123"
    assert row[2] == 0


def test_fetch_all(db):
    """Testa SELECT com vários resultados usando fetch_all."""
    users = [
        ("ana", "111", 0),
        ("bia", "222", 0),
        ("gih", "333", 1),
    ]

    for u in users:
        db.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            u,
        )

    rows = db.fetch_all("SELECT username FROM users ORDER BY username")
    usernames = [r[0] for r in rows]

    assert usernames == ["ana", "bia", "gih"]


def test_update(db):
    """Testa UPDATE."""
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("gih", "123", 0),
    )

    db.execute(
        "UPDATE users SET password=? WHERE username=?",
        ("abcd", "gih"),
    )

    row = db.fetch_one(
        "SELECT password FROM users WHERE username=?",
        ("gih",),
    )

    assert row[0] == "abcd"


def test_delete(db):
    """Testa DELETE."""
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("gih", "123", 0),
    )

    db.execute("DELETE FROM users WHERE username=?", ("gih",))

    row = db.fetch_one(
        "SELECT * FROM users WHERE username=?",
        ("gih",),
    )

    assert row is None


def test_last_insert_id(db):
    """Testa last_insert_id."""
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("ana", "111", 0),
    )

    last_id = db.last_insert_id(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("bia", "222", 0),
    )

    assert isinstance(last_id, int)

    row = db.fetch_one(
        "SELECT username FROM users WHERE id=?",
        (last_id,),
    )
    assert row[0] == "bia"
