import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_caca_emoji_route_no_form(game, monkeypatch):
    monkeypatch.setattr(
        "app.controllers.game_controller.random.randint",
        lambda a, b: 5
    )
    res = game.caca_emoji_route(user_id=1, form_data=None)

    assert res["alvo_idx"] == 5
    assert res["erros"] == 0
    assert res["fim"] is False

def test_caca_emoji_hit(game):
    res = game.caca_emoji(user_id=10, escolha_idx=2, alvo_idx=2, erros=0)

    assert res["fim"] is True
    assert "encontrou" in res["mensagem"].lower()
    
    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 10  
    assert args[1] == 10 

def test_caca_emoji_miss_and_end(game):
    r1 = game.caca_emoji(user_id=None, escolha_idx=0, alvo_idx=3, erros=0)
    assert r1["fim"] is False
    assert r1["erros"] == 1

    r2 = game.caca_emoji(user_id=None, escolha_idx=0, alvo_idx=3, erros=2)
    assert r2["fim"] is True
    assert "fim" in r2["mensagem"].lower()

    game.players.add_score_by_user_id.assert_not_called()
