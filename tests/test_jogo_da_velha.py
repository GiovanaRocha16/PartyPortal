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
    assert res["tabuleiro"] == ["-"] * 9
    assert "Sua vez" in res["mensagem"]


def test_jogo_da_velha_invalid_move(game):
    tab = ["X", "-", "-", "-", "-", "-", "-", "-", "-"]
    res = game.jogo_da_velha(user_id=1, tabuleiro=tab.copy(), jogada=0)
    assert "Escolha uma casa vazia" in res["mensagem"]


def test_jogo_da_velha_player_wins_and_score(game):
    tab = ["X", "X", "-", "-", "-", "-", "-", "-", "-"]
    res = game.jogo_da_velha(user_id=5, tabuleiro=tab.copy(), jogada=2)

    assert "venceu" in res["mensagem"]
    assert res["tabuleiro"][2] == "X"

    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 5
    assert args[1] == 10


def test_jogo_da_velha_bot_moves(game, monkeypatch):
    """
    Testa se o bot faz uma jogada válida após o jogador.
    """
    tab = ["X", "O", "X",
           "X", "O", "-",
           "O", "-", "-"]

    # casas vazias: 5, 7, 8
    monkeypatch.setattr("random.choice", lambda x: 5)

    res = game.jogo_da_velha(user_id=None, tabuleiro=tab.copy(), jogada=8)

    assert "mensagem" in res
    assert "tabuleiro" in res
    assert res["tabuleiro"][8] == "X"  # jogada do jogador
    assert res["tabuleiro"][5] == "O"  # jogada do bot
