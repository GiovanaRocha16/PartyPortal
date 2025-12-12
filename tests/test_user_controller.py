import pytest
from unittest.mock import patch, MagicMock
from app.controllers.user_controller import UserController


# ----------------------------------------------------
# register()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
@patch("app.controllers.user_controller.PlayerController")
def test_register_success(mock_player_ctrl, mock_user):
    ctrl = UserController()

    # usuário não existe
    mock_user.exists.return_value = False

    # simulando criação do user
    user_instance = MagicMock()
    user_instance.id = 10
    user_instance.to_dict.return_value = {"id": 10, "username": "gih", "is_admin": 0}
    mock_user.return_value = user_instance

    result = ctrl.register({"username": "gih", "password": "123"})

    assert result["ok"] is True
    assert result["redirect"] == "/home"

    mock_user.exists.assert_called_once_with(username="gih")
    mock_user.return_value.save.assert_called_once()
    mock_player_ctrl.return_value.create_player_for_user.assert_called_once_with(10)


def test_register_username_too_short():
    ctrl = UserController()

    result = ctrl.register({"username": "aa", "password": "123"})

    assert result == {"error": "Nome muito curto"}


@patch("app.controllers.user_controller.User")
def test_register_username_exists(mock_user):
    ctrl = UserController()

    mock_user.exists.return_value = True

    result = ctrl.register({"username": "gih", "password": "123"})

    assert result == {"error": "Usuário já existe"}
    mock_user.exists.assert_called_once_with(username="gih")


# ----------------------------------------------------
# list_users()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_list_users(mock_user):
    ctrl = UserController()

    user1 = MagicMock()
    user1.to_dict.return_value = {"id": 1}

    user2 = MagicMock()
    user2.to_dict.return_value = {"id": 2}

    mock_user.all.return_value = [user1, user2]

    result = ctrl.list_users()

    assert result == [{"id": 1}, {"id": 2}]


# ----------------------------------------------------
# login()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_login_success_user(mock_user):
    ctrl = UserController()

    user_instance = MagicMock()
    user_instance.to_dict.return_value = {"id": 1, "is_admin": 0}

    mock_user.authenticate.return_value = user_instance

    result = ctrl.login("gih", "123")

    assert result["ok"] is True
    assert result["redirect"] == "/home"


@patch("app.controllers.user_controller.User")
def test_login_success_admin(mock_user):
    ctrl = UserController()

    user_instance = MagicMock()
    user_instance.to_dict.return_value = {"id": 1, "is_admin": 1}

    mock_user.authenticate.return_value = user_instance

    result = ctrl.login("gih", "123")

    assert result["redirect"] == "/admin/dashboard"


@patch("app.controllers.user_controller.User")
def test_login_invalid(mock_user):
    ctrl = UserController()

    mock_user.authenticate.return_value = None

    result = ctrl.login("x", "y")

    assert result == {"error": "Credenciais inválidas"}


# ----------------------------------------------------
# logout()
# ----------------------------------------------------
def test_logout():
    ctrl = UserController()
    assert ctrl.logout() == {"ok": True, "redirect": "/login"}


# ----------------------------------------------------
# make_admin()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_make_admin_success(mock_user):
    ctrl = UserController()

    user = MagicMock()
    user.id = 50

    mock_user.get_by_username.return_value = user

    result = ctrl.make_admin("gih")

    assert result == {"ok": True}
    mock_user.set_admin.assert_called_once_with(50, True)


@patch("app.controllers.user_controller.User")
def test_make_admin_not_found(mock_user):
    ctrl = UserController()

    mock_user.get_by_username.return_value = None

    result = ctrl.make_admin("nada")

    assert result == {"error": "Usuário não encontrado"}


# ----------------------------------------------------
# check_admin()
# ----------------------------------------------------
def test_check_admin_true():
    ctrl = UserController()
    assert ctrl.check_admin({"is_admin": 1}) is True


def test_check_admin_false():
    ctrl = UserController()
    assert ctrl.check_admin({"is_admin": 0}) is False


def test_check_admin_none():
    ctrl = UserController()
    assert ctrl.check_admin(None) is False


# ----------------------------------------------------
# get_user_by_id()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_get_user_by_id(mock_user):
    ctrl = UserController()

    u = MagicMock()
    u.to_dict.return_value = {"id": 10}
    mock_user.get_by_id.return_value = u

    result = ctrl.get_user_by_id(10)

    assert result == {"id": 10}


@patch("app.controllers.user_controller.User")
def test_get_user_by_id_none(mock_user):
    ctrl = UserController()

    mock_user.get_by_id.return_value = None

    assert ctrl.get_user_by_id(10) is None


# ----------------------------------------------------
# add_user()  (só chama register)
# ----------------------------------------------------
@patch.object(UserController, "register")
def test_add_user(mock_register):
    ctrl = UserController()

    ctrl.add_user("gih", "123")

    mock_register.assert_called_once_with({"username": "gih", "password": "123"})


# ----------------------------------------------------
# update_user()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_update_user_success(mock_user):
    ctrl = UserController()

    user = MagicMock()
    mock_user.get_by_id.return_value = user

    result = ctrl.update_user(10, username="novo", password="123")

    assert result == {"ok": True}
    assert user.username == "novo"
    assert user.password == "123"
    user.save.assert_called_once()


@patch("app.controllers.user_controller.User")
def test_update_user_not_found(mock_user):
    ctrl = UserController()

    mock_user.get_by_id.return_value = None

    result = ctrl.update_user(10)

    assert result == {"error": "Usuário não encontrado"}


# ----------------------------------------------------
# delete_user()
# ----------------------------------------------------
@patch("app.controllers.user_controller.User")
def test_delete_user_success(mock_user):
    ctrl = UserController()

    user = MagicMock()
    mock_user.get_by_id.return_value = user

    result = ctrl.delete_user(5)

    assert result == {"ok": True}
    user.delete.assert_called_once()


@patch("app.controllers.user_controller.User")
def test_delete_user_not_found(mock_user):
    ctrl = UserController()

    mock_user.get_by_id.return_value = None

    result = ctrl.delete_user(5)

    assert result == {"error": "Usuário não encontrado"}
