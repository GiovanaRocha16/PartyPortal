from app.models.model import Model

class User(Model):
    table = "users"
    fields = ["id", "username", "password", "is_admin"]

    # ----------------- Metodos de classe -----------------
    @classmethod
    def authenticate(cls, username, password):
        query = "SELECT * FROM users WHERE username=? AND password=?"
        row = cls.db.fetch_one(query, (username, password))
        return cls.from_row(row)

    @classmethod
    def exists(cls, username):
        query = "SELECT id FROM users WHERE username=?"
        row = cls.db.fetch_one(query, (username,))
        return row is not None

    @classmethod
    def set_admin(cls, user_id, is_admin=True):
        cls.update(user_id, is_admin=int(is_admin))

    @classmethod
    def get_by_username(cls, username):
        query = "SELECT * FROM users WHERE username=?"
        row = cls.db.fetch_one(query, (username,))
        return cls.from_row(row)
    
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id=?"
        row = cls.db.fetch_one(query, (user_id,))
        return cls.from_row(row)

