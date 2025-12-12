import pytest
from unittest.mock import patch, MagicMock
from app.controllers.session_manager import SessionManager
from datetime import datetime


# ------------------------------------------------------
# create_session()
# ------------------------------------------------------
@patch("app.controllers.session_manager.db")
@patch("app.controllers.session_manager.uuid")
def test_create_session(mock_uuid, mock_db):
    mock_uuid.uuid4.return_value = "ABC-123"

    result = SessionManager.create_session({"id": 10})

    assert result == "ABC-123"

    mock_db.execute.assert_called_once()
    call_args = mock_db.execute.call_args[0]

    assert call_args[0].startswith("INSERT INTO sessions")
    assert call_args[1][0] == "ABC-123"
    assert call_args[1][1] == 10


# ------------------------------------------------------
# get_session() – sessão encontrada
# ------------------------------------------------------
@patch("app.controllers.session_manager.db")
def test_get_session_success(mock_db):
    mock_db.fetch_one.side_effect = [
        ("ABC", 5),
        (5, "gih", 1),
    ]

    result = SessionManager.get_session("ABC")

    assert result == {
        "id": 5,
        "username": "gih",
        "is_admin": True
    }

    assert mock_db.fetch_one.call_count == 2


# ------------------------------------------------------
# get_session() – sessão NÃO encontrada
# ------------------------------------------------------
@patch("app.controllers.session_manager.db")
def test_get_session_not_found(mock_db):
    mock_db.fetch_one.return_value = None

    result = SessionManager.get_session("INVALID")

    assert result is None
    mock_db.fetch_one.assert_called_once()


# ------------------------------------------------------
# delete_session()
# ------------------------------------------------------
@patch("app.controllers.session_manager.db")
def test_delete_session(mock_db):
    SessionManager.delete_session("XYZ")

    mock_db.execute.assert_called_once_with(
        "DELETE FROM sessions WHERE session_id = ?",
        ("XYZ",)
    )


# ------------------------------------------------------
# is_admin() – usuário é admin
# ------------------------------------------------------
@patch.object(SessionManager, "get_session")
def test_is_admin_true(mock_get_session):
    mock_get_session.return_value = {"is_admin": True}

    assert SessionManager.is_admin("SID") is True


# ------------------------------------------------------
# is_admin() – usuário não é admin
# ------------------------------------------------------
@patch.object(SessionManager, "get_session")
def test_is_admin_false(mock_get_session):
    mock_get_session.return_value = {"is_admin": False}

    assert SessionManager.is_admin("SID") is False


# ------------------------------------------------------
# is_admin() – sessão inexistente
# ------------------------------------------------------
@patch.object(SessionManager, "get_session")
def test_is_admin_missing_session(mock_get_session):
    mock_get_session.return_value = None

    assert SessionManager.is_admin("SID") is False


# ------------------------------------------------------
# list_sessions()
# ------------------------------------------------------
@patch("app.controllers.session_manager.db")
def test_list_sessions(mock_db):
    mock_db.fetch_all.return_value = [
        ("S1", 100),
        ("S2", 200),
    ]

    mock_db.fetch_one.side_effect = [
        ("gih", 1),
        ("joao", 0),
    ]

    result = SessionManager.list_sessions()

    assert result == [
        ("S1", "gih", True),
        ("S2", "joao", False),
    ]

    assert mock_db.fetch_all.call_count == 1
    assert mock_db.fetch_one.call_count == 2
