import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_jogo_da_velha_route_initial(game):
    res = game.jogo_da_velha_route(user_id=1, form_data=None)
    assert res["tabuleiro"] == ["-"]*9
    assert "Sua vez" in res["mensagem"]

def test_jogo_da_velha_invalid_move(game):
    tab = ["X","-","-","-","-","-","-","-","-"]
    res = game.jogo_da_velha(user_id=1, tabuleiro=tab.copy(), jogada=0)
    assert "Escolha uma casa vazia" in res["mensagem"]

def test_jogo_da_velha_player_wins_and_score(game):
    tab = ["X","X","-","-","-","-","-","-","-"]
    res = game.jogo_da_velha(user_id=5, tabuleiro=tab.copy(), jogada=2)
    assert "venceu" in res["mensagem"]
    game.players.add_score_by_user_id.assert_called_once_with(5, 10)

def test_jogo_da_velha_bot_moves_and_possible_bot_win(game, monkeypatch):
    tab = ["X","O","X","X","O","O","O","X","-"]
    monkeypatch.setattr("random.choice", lambda x: 8)
    res = game.jogo_da_velha(user_id=None, tabuleiro=tab.copy(), jogada=8)
    assert "mensagem" in res
    assert "tabuleiro" in res
