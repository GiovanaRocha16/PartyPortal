from app.models.model import Model

class Player(Model):
    table = "players"
    fields = ["id", "user_id", "score"]

    # ----------------- Metodos de clase -----------------
    @classmethod
    def create_for_user(cls, user_id):
        player = cls.get_by_user(user_id)
        if player:
            return player
        new_player = cls(user_id=user_id, score=0)
        new_player.save()
        return new_player

    @classmethod
    def get_by_user(cls, user_id):
        query = f"SELECT * FROM {cls.table} WHERE user_id=?"
        row = cls.db.fetch_one(query, (user_id,))
        return cls.from_row(row)

    @classmethod
    def delete_by_user_id(cls, user_id):
        player = cls.get_by_user(user_id)
        if player:
            player.delete()

    # ----------------- Metodos instanciados -----------------
    def add_score(self, amount):
        self.score += amount
        self.save()

    def to_public_dict(self, username):
        return {
            "user_id": self.user_id,
            "username": username,
            "score": self.score
        }

