import pytest
from unittest.mock import MagicMock
from app.controllers.game_controller import GameController

@pytest.fixture
def game():
    g = GameController()
    g.players = MagicMock()
    return g

def test_confeiteiro_route_no_form(game):
    res = game.confeiteiro_route(user_id=1, form_data=None)
    assert res == {"resultado": None}

def test_confeiteiro_known_recipe_awards(game):
    res = game.confeiteiro(user_id=7, ing1="Chocolate", ing2="Morango", ing3="Leite")
    assert "delicioso" in res["resultado"]

    game.players.add_score_by_user_id.assert_called_once()
    args, kwargs = game.players.add_score_by_user_id.call_args
    assert args[0] == 7
    assert args[1] == 5

def test_confeiteiro_bad_recipe_no_award(game):
    res = game.confeiteiro(user_id=7, ing1="Pimenta", ing2="Alho", ing3="Limão")
    assert "🤢" in res["resultado"]
    game.players.add_score_by_user_id.assert_not_called()
