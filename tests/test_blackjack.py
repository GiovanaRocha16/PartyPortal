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

    assert "jogador" in res
    assert "bot" in res
    assert res["fim"] is False


def test_blackjack_comprar_busts(game, monkeypatch):
    jogador = [10, 10]
    bot = [5, 5]

    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: 2
    )

    res = game.mini_blackjack_jogar(
        user_id=1,
        acao="comprar",
        jogador=jogador.copy(),
        bot=bot.copy()
    )

    assert res["fim"] is True
    assert "estour" in res["resultado"].lower()
    game.players.add_score_by_user_id.assert_not_called()


def test_blackjack_parar_bot_busts(game, monkeypatch):
    jogador = [10, 8]   # 18
    bot = [10, 6]       # 16

    seq = iter([10])   # bot compra e estoura
    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: next(seq)
    )

    res = game.mini_blackjack_jogar(
        user_id=42,
        acao="parar",
        jogador=jogador.copy(),
        bot=bot.copy()
    )

    assert res["fim"] is True
    assert ("bot estour" in res["resultado"].lower()) or ("venceu" in res["resultado"].lower())

    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 42
    assert args[1] == 10


def test_blackjack_parar_player_wins(game, monkeypatch):
    jogador = [10, 10]  # 20
    bot = [10, 8]       # 18

    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: 1
    )

    res = game.mini_blackjack_jogar(
        user_id=7,
        acao="parar",
        jogador=jogador.copy(),
        bot=bot.copy()
    )

    assert res["fim"] is True
    assert "venceu" in res["resultado"].lower()

    game.players.add_score_by_user_id.assert_called_once()
    args, _ = game.players.add_score_by_user_id.call_args
    assert args[0] == 7
    assert args[1] == 10


def test_blackjack_parar_player_loses_or_tie(game, monkeypatch):
    jogador = [10, 8]  # 18
    bot = [10, 10]     # 20

    monkeypatch.setattr(
        "app.controllers.game_controller.random.choice",
        lambda x: 1
    )

    res = game.mini_blackjack_jogar(
        user_id=99,
        acao="parar",
        jogador=jogador.copy(),
        bot=bot.copy()
    )

    assert res["fim"] is True
    assert ("perdeu" in res["resultado"].lower()) or ("empate" in res["resultado"].lower())
