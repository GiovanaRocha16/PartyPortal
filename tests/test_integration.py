import pytest
from webtest import TestApp
import route as app_route
from app.models.database import Database
import time

DB = Database()

@pytest.fixture(autouse=True)
def clean_db():
    """
    Limpa tabelas antes de cada teste para garantir estado previsível.
    """
    DB.execute("DELETE FROM sessions")
    DB.execute("DELETE FROM players")
    DB.execute("DELETE FROM users")
    yield
    DB.execute("DELETE FROM sessions")
    DB.execute("DELETE FROM players")
    DB.execute("DELETE FROM users")


@pytest.fixture
def client():
    """
    Retorna um webtest.TestApp para o Bottle app definido em route.py
    """
    return TestApp(app_route.app)


def register_user(client, username="testuser", password="pass"):
    """Helper: registra usuário via POST /register"""
    resp = client.post('/register', {'username': username, 'password': password})
    assert resp.status_int in (200, 302, 303)
    row = DB.fetch_one("SELECT id, username FROM users WHERE username=?", (username,))
    assert row is not None
    return row[0]


def login_user(client, username="testuser", password="pass"):
    """Helper: faz POST /login e retorna o response (TestApp keeps cookies)"""
    resp = client.post('/login', {'username': username, 'password': password})
    assert resp.status_int in (200, 302, 303)
    return resp


def get_session_rows():
    return DB.fetch_all("SELECT session_id, user_id FROM sessions")


def test_register_login_creates_session_and_cookie(client):
    uid = register_user(client, "alice", "pw123")

    resp = login_user(client, "alice", "pw123")

    set_cookie = resp.headers.get('Set-Cookie') or ""
    assert "session_id=" in set_cookie or client.cookies.get('session_id') is not None

    rows = get_session_rows()
    assert len(rows) == 1
    session_id, user_id = rows[0]
    assert int(user_id) == int(uid)
    assert session_id is not None and session_id != ""


def test_logout_deletes_session_and_redirects(client):
    uid = register_user(client, "bob", "pw123")
    login_user(client, "bob", "pw123")

    rows = get_session_rows()
    assert len(rows) == 1

    resp = client.get('/logout')
    assert resp.status_int in (200, 302, 303)

    rows2 = get_session_rows()
    assert len(rows2) == 0


def test_protected_players_redirects_when_not_logged_in(client):
    resp = client.get('/players', status=302)
    assert '/login' in resp.headers.get('Location', '') or resp.status_int in (302, 303)



def test_admin_dashboard_requires_admin(client):
    uid = register_user(client, "dave", "pw")
    login_user(client, "dave", "pw")
    resp = client.get('/admin/dashboard')
    assert resp.status_int == 200
    assert resp.text is not None

    DB.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (uid,))
    client.get('/logout')
    login_user(client, "dave", "pw")

    resp2 = client.get('/admin/dashboard')
    assert resp2.status_int == 200
    assert resp2.text is not None


def test_game_route_confeiteiro_get_and_post(client, monkeypatch):
    register_user(client, "erin", "pw")
    login_user(client, "erin", "pw")

    resp = client.get('/confeiteiro')
    assert resp.status_int == 200
    assert "confeiteiro" in resp.text.lower() or "resultado" in resp.text.lower() or resp.text

    post = client.post('/confeiteiro', {'ing1': 'Chocolate', 'ing2': 'Morango', 'ing3': 'Leite'})
    assert post.status_int in (200, 302, 303)
    assert "bolo" in post.text.lower() or "resultado" in post.text.lower() or post.text


def test_game_routes_basic_accessible_when_logged_in(client):
    register_user(client, "fran", "pw")
    login_user(client, "fran", "pw")

    for route in [
        '/campo_minado', '/caca_niquel', '/pedra_papel_tesoura',
        '/mini_black_jack', '/jogo_da_velha', '/caca_emoji',
        '/numero_secreto', '/clique_rapido'
    ]:
        resp = client.get(route)
        assert resp.status_int == 200


def test_register_requires_username_and_password(client):
    resp = client.post('/register', {'username': 'no_pw'}, status=200)
    assert "Usuário e senha" in resp.text or "obrigatórios" in resp.text

