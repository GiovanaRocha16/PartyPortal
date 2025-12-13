import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_campo_minado_route_no_form_returns_state(game, monkeypatch):
    monkeypatch.setattr(
        "app.controllers.game_controller.random.randint",
        lambda a, b: 4
    )

    res = game.campo_minado_route(user_id=1, form_data=None)

    assert res["resultado"] is None
    assert isinstance(res["clicados"], list)
    assert res["bomba"] == 4
    assert res["acabou"] is False

def test_campo_minado_explode(game):
    out = game.campo_minado(user_id=1, escolha=3, clicados=[], bomba=3)

    assert "boom" in out["resultado"].lower()
    assert out["acabou"] is True

def test_campo_minado_win_and_score(game):
    clicados = [1, 2, 3, 4, 5, 6, 7]

    out = game.campo_minado(user_id=2, escolha=8, clicados=clicados, bomba=9)

    assert "parabéns" in out["resultado"].lower()
    assert out["acabou"] is True

    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 2
    assert args[1] == 10

def test_campo_minado_continue(game):
    out = game.campo_minado(user_id=None, escolha=1, clicados=[], bomba=9)

    assert "tentativas seguras" in out["resultado"].lower()
    assert out["acabou"] is False
