from app.models.player import Player

class PlayerController:
    """
    Controller responsável por operações de player
    """

    def create_player_for_user(self, user_id):
        return Player.create_for_user(user_id)

    def add_score_by_user_id(self, user_id, amount, websocket_manager=None, user_ctrl=None):
        player = Player.get_by_user(user_id)
        if player:
            player.add_score(amount)
            if websocket_manager and user_ctrl:
                websocket_manager.broadcast_ranking(self, user_ctrl)
            return player
        return None

    def list_players(self):
        return Player.all()

    def get_stats_by_user_id(self, user_id):
        return Player.get_by_user(user_id)

    def get_player_position(self, user_id):
        players = sorted(self.list_players(), key=lambda p: p.score, reverse=True)
        player = self.get_stats_by_user_id(user_id)
        position = None
        if player:
            for idx, p in enumerate(players, start=1):
                if p.user_id == user_id:
                    position = idx
                    break
        return player, position


    def delete_player_by_user_id(self, user_id):
        Player.delete_by_user_id(user_id)

    def get_ranking(self, user_ctrl):
        players = Player.all()
        players_sorted = sorted(players, key=lambda p: p.score, reverse=True)

        ranking = []
        for p in players_sorted:
            user = user_ctrl.get_user_by_id(p.user_id)
            username = user["username"] if user else "???"
            ranking.append(p.to_public_dict(username))

        return ranking


