from app.models.user import User
from app.controllers.player_controller import PlayerController

class UserController:
    """
    Controller responsável por regras de negócio do usuário
    """

    def __init__(self):
        self.player_ctrl = PlayerController()

    def register(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or len(username) < 3:
            return {"error": "Nome muito curto"}

        if User.exists(username=username):
            return {"error": "Usuário já existe"}

        user = User(username=username, password=password, is_admin=0)
        user.save()

        self.player_ctrl.create_player_for_user(user.id)

        return {"ok": True, "redirect": "/home", "user": user.to_dict()}
    
    def list_users(self):
        return [u.to_dict() for u in User.all()]

    def login(self, username, password):
        user = User.authenticate(username, password)
        if not user:
            return {"error": "Credenciais inválidas"}

        user_dict = user.to_dict()
        if user_dict.get("is_admin"):
            redirect = "/admin/dashboard"
        else:
            redirect = "/home"

        return {"ok": True, "redirect": redirect, "user": user_dict}

    def logout(self):
        return {"ok": True, "redirect": "/login"}
    
    def make_admin(self, username):
        user = User.get_by_username(username)
        if not user:
            return {"error": "Usuário não encontrado"}
        User.set_admin(user.id, True)
        return {"ok": True}

    def check_admin(self, user_dict):
        return bool(user_dict.get("is_admin")) if user_dict else False
    
    def get_user_by_id(self, user_id):
        user = User.get_by_id(user_id)
        return user.to_dict() if user else None
    
    def add_user(self, username, password):
        return self.register({"username": username, "password": password})
    
    def update_user(self, user_id, username=None, password=None):
        user = User.get_by_id(user_id)
        if not user:
            return {"error": "Usuário não encontrado"}
        if username:
            user.username = username
        if password:
            user.password = password
        user.save()
        return {"ok": True}

    def delete_user(self, user_id):
        user = User.get_by_id(user_id)
        if not user:
            return {"error": "Usuário não encontrado"}
        user.delete()
        return {"ok": True}


