import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_blackjack_route_initial(game):
    res = game.blackjack_route(user_id=1, form_data=None)
    assert "jogador" in res and "bot" in res and res["fim"] is False

def test_blackjack_comprar_busts(game, monkeypatch):
    jogador = [10,10]
    bot = [5,5]
    monkeypatch.setattr("random.choice", lambda x: 2)
    res = game.mini_blackjack_jogar(user_id=1, acao="comprar", jogador=jogador.copy(), bot=bot.copy())
    assert res["fim"] is True
    assert "estourou" in res["resultado"]
    game.players.add_score_by_user_id.assert_not_called()

def test_blackjack_parar_bot_busts(game, monkeypatch):
    jogador = [10,8]   # 18
    bot = [10,6]       # 16 -> estoura
    seq = iter([10])   # 10 -> 26
    monkeypatch.setattr("random.choice", lambda x: next(seq))
    res = game.mini_blackjack_jogar(user_id=42, acao="parar", jogador=jogador.copy(), bot=bot.copy())
    assert res["fim"] is True
    assert ("bot estourou" in res["resultado"].lower()) or ("você venceu" in res["resultado"].lower())
    game.players.add_score_by_user_id.assert_called_once_with(42, 10)

def test_blackjack_parar_player_wins(game, monkeypatch):
    jogador = [10,10]  # 20
    bot = [10,8]       # 18
    monkeypatch.setattr("random.choice", lambda x: 1)
    res = game.mini_blackjack_jogar(user_id=7, acao="parar", jogador=jogador.copy(), bot=bot.copy())
    assert res["fim"] is True
    assert "Você venceu" in res["resultado"] or "você venceu" in res["resultado"].lower()
    game.players.add_score_by_user_id.assert_called_once_with(7, 10)

def test_blackjack_parar_player_loses_or_tie(game, monkeypatch):
    jogador = [10,8]  # 18
    bot = [10,10]     # 20
    monkeypatch.setattr("random.choice", lambda x: 1)
    res = game.mini_blackjack_jogar(user_id=99, acao="parar", jogador=jogador.copy(), bot=bot.copy())
    assert res["fim"] is True
    assert ("perdeu" in res["resultado"].lower()) or ("empate" in res["resultado"].lower())
