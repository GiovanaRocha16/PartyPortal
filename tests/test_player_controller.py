import pytest
from unittest.mock import patch, MagicMock
from app.controllers.player_controller import PlayerController


@pytest.fixture
def controller():
    return PlayerController()


# -----------------------------------------------------
# create_player_for_user()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_create_player_for_user(mock_player, controller):
    mock_player.create_for_user.return_value = "PLAYER_OK"

    result = controller.create_player_for_user(10)

    mock_player.create_for_user.assert_called_once_with(10)
    assert result == "PLAYER_OK"


# -----------------------------------------------------
# add_score_by_user_id()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_add_score_by_user_id_success(mock_player, controller):
    mocked_player = MagicMock()
    mock_player.get_by_user.return_value = mocked_player

    result = controller.add_score_by_user_id(5, 30)

    mock_player.get_by_user.assert_called_once_with(5)
    mocked_player.add_score.assert_called_once_with(30)
    assert result is mocked_player


@patch("app.controllers.player_controller.Player")
def test_add_score_by_user_id_not_found(mock_player, controller):
    mock_player.get_by_user.return_value = None

    result = controller.add_score_by_user_id(5, 30)

    assert result is None
    mock_player.get_by_user.assert_called_once_with(5)


# -----------------------------------------------------
# list_players()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_list_players(mock_player, controller):
    mock_player.all.return_value = ["A", "B"]

    result = controller.list_players()

    mock_player.all.assert_called_once()
    assert result == ["A", "B"]


# -----------------------------------------------------
# get_stats_by_user_id()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_get_stats_by_user_id(mock_player, controller):
    mock_player.get_by_user.return_value = "PLAYER_DATA"

    result = controller.get_stats_by_user_id(22)

    mock_player.get_by_user.assert_called_once_with(22)
    assert result == "PLAYER_DATA"


# -----------------------------------------------------
# get_player_position()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_get_player_position_found(mock_player, controller):
    p1 = MagicMock(user_id=1, score=50)
    p2 = MagicMock(user_id=2, score=30)
    p3 = MagicMock(user_id=3, score=10)

    mock_player.all.return_value = [p2, p1, p3]  # Fora de ordem proposital
    mock_player.get_by_user.return_value = p2

    player, pos = controller.get_player_position(2)

    assert player is p2
    assert pos == 2


@patch("app.controllers.player_controller.Player")
def test_get_player_position_not_found(mock_player, controller):
    mock_player.all.return_value = []
    mock_player.get_by_user.return_value = None

    player, pos = controller.get_player_position(999)

    assert player is None
    assert pos is None


# -----------------------------------------------------
# delete_player_by_user_id()
# -----------------------------------------------------
@patch("app.controllers.player_controller.Player")
def test_delete_player_by_user_id(mock_player, controller):
    controller.delete_player_by_user_id(10)

    mock_player.delete_by_user_id.assert_called_once_with(10)
