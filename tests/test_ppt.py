import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_ppt_route_no_form(game):
    res = game.ppt_route(user_id=1, form_data=None)
    assert res == {"escolha": None, "bot": None, "resultado": None}

def test_ppt_empate(game, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: "Pedra")
    res = game.pedra_papel_tesoura(user_id=1, escolha="Pedra")
    assert "Empate" in res["resultado"]

def test_ppt_win_and_score(game, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: "Tesoura")
    res = game.pedra_papel_tesoura(user_id=4, escolha="Pedra")
    assert "ganhou" in res["resultado"]
    game.players.add_score_by_user_id.assert_called_once_with(4, 5)

def test_ppt_loss(game, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: "Papel")
    res = game.pedra_papel_tesoura(user_id=None, escolha="Pedra")
    assert "perdeu" in res["resultado"]
