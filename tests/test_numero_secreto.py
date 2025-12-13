import pytest
from unittest.mock import MagicMock, call
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g


def test_numero_secreto_route_no_form(game, monkeypatch):
    monkeypatch.setattr("random.randint", lambda a, b: 13)
    res = game.numero_secreto_route(user_id=1, form_data=None)
    assert res["numero"] == 13
    assert res["tentativas"] == 0


def test_numero_secreto_hit_awards(game):
    res = game.numero_secreto(user_id=2, numero=7, tentativas=0, chute=7)
    assert res["fim"] is True
    assert res["tentativas"] == 1

    assert game.players.add_score_by_user_id.called

    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 2
    assert args[1] == 15


def test_numero_secreto_lower_or_higher(game):
    r1 = game.numero_secreto(user_id=None, numero=20, tentativas=0, chute=5)
    assert "maior" in r1["mensagem"].lower()

    r2 = game.numero_secreto(user_id=None, numero=5, tentativas=1, chute=10)
    assert "menor" in r2["mensagem"].lower()
