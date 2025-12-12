import pytest
from unittest.mock import MagicMock, patch
from app.controllers.application import Application


@pytest.fixture
def app_instance():
    """Cria Application com controllers mockados."""
    app = Application()

    # mock dos controllers
    app.user_controller = MagicMock()
    app.player_controller = MagicMock()
    app.game_controller = MagicMock()
    app.session_manager = MagicMock()

    return app


# -----------------------------
# TESTE: render()
# -----------------------------
@patch("app.controllers.application.template")
def test_render_existing_page(mock_template, app_instance):
    app_instance.pages = {"home": lambda: "HOME_OK"}
    result = app_instance.render("home")
    assert result == "HOME_OK"


@patch("app.controllers.application.template")
def test_render_missing_page(mock_template, app_instance):
    mock_template.return_value = "404 PAGE"
    result = app_instance.render("not_exists")
    mock_template.assert_called_once()
    assert result == "404 PAGE"


# -----------------------------
# TESTE: login_user()
# -----------------------------
def test_login_user_creates_session(app_instance):
    app_instance.session_manager.create_session.return_value = "SID123"

    session = app_instance.login_user({"id": 1})
    assert session == "SID123"
    app_instance.session_manager.create_session.assert_called_once()


# -----------------------------
# TESTE: logout_user()
# -----------------------------
@patch("app.controllers.application.request")
def test_logout_user(mock_request, app_instance):
    mock_request.get_cookie.return_value = "SID123"

    app_instance.logout_user()
    app_instance.session_manager.delete_session.assert_called_once_with("SID123")


# -----------------------------
# TESTE: current_user()
# -----------------------------
@patch("app.controllers.application.request")
def test_current_user(mock_request, app_instance):
    mock_request.get_cookie.return_value = "SID999"
    app_instance.session_manager.get_session.return_value = {"id": 1}

    result = app_instance.current_user()
    assert result == {"id": 1}
    app_instance.session_manager.get_session.assert_called_once_with("SID999")


# -----------------------------
# TESTE: check_permission()
# -----------------------------
def test_check_permission_without_user(app_instance):
    app_instance.current_user = MagicMock(return_value=None)
    assert app_instance.check_permission() is False


def test_check_permission_basic(app_instance):
    app_instance.current_user = MagicMock(return_value={"id": 1})
    assert app_instance.check_permission() is True


def test_check_permission_admin(app_instance):
    app_instance.current_user = MagicMock(return_value={"id": 1})
    app_instance.user_controller.check_admin.return_value = True

    assert app_instance.check_permission(admin_required=True) is True


# -----------------------------
# TESTE: require_admin()
# -----------------------------
def test_require_admin_denied(app_instance):
    app_instance.current_user = MagicMock(return_value=None)

    result = app_instance.require_admin()
    assert isinstance(result, tuple)  # (response, 403)
    assert result[1] == 403


def test_require_admin_success(app_instance):
    app_instance.current_user = MagicMock(return_value={"id": 10})
    app_instance.user_controller.check_admin.return_value = True

    result = app_instance.require_admin()
    assert result == {"id": 10}


# -----------------------------
# TESTE: admin_delete_user()
# -----------------------------
def test_admin_delete_user(app_instance):
    app_instance.require_admin = MagicMock(return_value={"id": 99})

    with patch("app.controllers.application.redirect") as mock_redirect:
        app_instance.admin_delete_user(5)
        app_instance.user_controller.delete_user.assert_called_once_with(5)
        app_instance.player_controller.delete_player_by_user_id.assert_called_once_with(5)
        mock_redirect.assert_called_once()


# -----------------------------
# TESTE: get_user_id()
# -----------------------------
def test_get_user_id(app_instance):
    app_instance.current_user = MagicMock(return_value={"id": 55})
    assert app_instance.get_user_id() == 55
