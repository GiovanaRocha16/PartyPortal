import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_caca_niquel_route_calls_game(game):
    res = game.caca_niquel_route(user_id=1, form_data={})
    assert "slots" in res
    assert "resultado" in res

def test_caca_niquel_win_and_score(game, monkeypatch):
    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: "7️⃣"
    )

    res = game.caca_niquel(user_id=3)

    assert "ganhou" in res["resultado"].lower()

    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 3
    assert args[1] == 5 

def test_caca_niquel_loss(game, monkeypatch):
    seq = iter(["🍒", "⭐", "🍉"])
    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: next(seq)
    )

    res = game.caca_niquel(user_id=3)

    assert "tente de novo" in res["resultado"].lower()
    game.players.add_score_by_user_id.assert_not_called()
