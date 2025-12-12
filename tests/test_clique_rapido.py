import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    # reset clicks_data to fresh state for each test
    g.clicks_data = {"count":0, "start":0}
    return g

def test_clique_rapido_route_no_form(game):
    res = game.clique_rapido_route(user_id=1, form_data=None)
    assert res == {"tempo": None, "cliques": 0}

def test_clique_rapido_reset(game):
    game.clicks_data = {"count":5, "start":123}
    res = game.clique_rapido(user_id=1, reset=True)
    assert res["cliques"] == 0

def test_clique_rapido_click_accumulates(game, monkeypatch):
    times = iter([1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0, 1006.0, 1007.0, 1008.0, 1009.0])
    monkeypatch.setattr("time.time", lambda: next(times))
    for i in range(9):
        r = game.clique_rapido(user_id=None, click=True)
        assert r["tempo"] is None
    r10 = game.clique_rapido(user_id=99, click=True)
    assert "tempo" in r10 and r10["cliques"] == 0
    game.players.add_score_by_user_id.assert_called_once_with(99, 15)
