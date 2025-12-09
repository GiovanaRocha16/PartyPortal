from bottle import template, redirect, request
from app.controllers.user_controller import UserController
from app.controllers.player_controller import PlayerController
from app.controllers.game_controller import GameController
from app.controllers.session_manager import SessionManager


class Application:
    def __init__(self):
        # Controllers
        self.user_controller = UserController()
        self.player_controller = PlayerController()
        self.game_controller = GameController()
        self.session_manager = SessionManager()

        # Mapa
        self.pages = {
            'home': self.home,
            'login': self.login_page,
            'register': self.register_page,
            'admin_dashboard': self.admin_dashboard
        }

    # -------------------------------------------
    # RENDER
    # -------------------------------------------
    def render(self, page, **kwargs):
        func = self.pages.get(page)
        if not func:
            return template('app/views/html/404')
        return func(**kwargs)

    def home(self, **kwargs):
        user = self.current_user()
        if user:
            player, position = self.player_controller.get_player_position(user["id"])
            user_score = player.score if player else 0
            return template(
                'app/views/html/home',
                username=user["username"],
                user_score=user_score,
                user_position=position,
                **kwargs
            )
        else:
            return template(
                'app/views/html/home',
                username=None,
                user_score=None,
                user_position=None,
                **kwargs
            )

    def login_page(self, erro=None, **kwargs):
        return template('app/views/html/login', erro=erro, **kwargs)

    def register_page(self, erro=None, **kwargs):
        return template('app/views/html/register', erro=erro, **kwargs)

    def access_denied(self):
        """Renderiza a página de acesso negado"""
        return template('app/views/html/access_denied')

    # -------------------------------------------
    # SESSÃO
    # -------------------------------------------
    def login_user(self, user_dict):
        """Cria sessão e retorna session_id"""
        return self.session_manager.create_session(user_dict)

    def logout_user(self):
        sid = request.get_cookie("session_id")
        if sid:
            self.session_manager.delete_session(sid)

    def current_user(self):
        sid = request.get_cookie("session_id")
        return self.session_manager.get_session(sid)

    def check_permission(self, admin_required=False):
        user = self.current_user()
        if not user:
            return False
        if admin_required:
            return self.user_controller.check_admin(user)
        return True

    def require_admin(self):
        user = self.current_user()
        if not user or not self.user_controller.check_admin(user):
            return self.access_denied(), 403
        return user

    # -------------------------------------------
    # ADMIN ROUTES
    # -------------------------------------------
    def admin_dashboard(self, **kwargs):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        usuarios = self.user_controller.list_users()
        players = self.player_controller.list_players()
        return template(
            'app/views/html/admin_dashboard',
            usuarios=usuarios,
            players=players,
            **kwargs
        )

    def admin_add_user(self, username, password):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        result = self.user_controller.register({"username": username, "password": password})
        if result.get("error"):
            return self.admin_dashboard(erro=result["error"])
        return redirect('/admin/dashboard')

    def admin_update_user(self, user_id, username, password):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        self.user_controller.update_user(user_id, username, password)
        return redirect('/admin/dashboard')

    def admin_delete_user(self, user_id):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        self.user_controller.delete_user(user_id)
        self.player_controller.delete_player_by_user_id(user_id)
        return redirect('/admin/dashboard')

    def admin_sessions(self):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        sessions = self.session_manager.list_sessions()
        return template('app/views/html/admin_sessions', sessions=sessions)

    def admin_delete_session(self, session_id):
        user = self.require_admin()
        if isinstance(user, tuple):
            return user

        self.session_manager.delete_session(session_id)
        return redirect('/admin/sessions')

    # -------------------------------------------
    # PLAYER ROUTES
    # -------------------------------------------
    def list_players(self, **kwargs):
        if not self.check_permission():
            return redirect("/login")
        players = self.player_controller.list_players()
        return template('app/views/html/players', players=players, **kwargs)

    def add_player(self):
        user = self.current_user()
        if not user:
            return redirect("/login")
        self.player_controller.create_player_for_user(user['id'], f"Player{user['id']}")
        return redirect('/players')

    def get_user_id(self):
        user = self.current_user()
        if not user:
            redirect("/login")
        return user["id"]

    # -------------------------------------------
    # GAMES ROUTES
    # -------------------------------------------
    def jogo_confeiteiro(self, user_id, form_data=None):
        state = self.game_controller.confeiteiro_route(user_id, form_data)
        return template('app/views/html/confeiteiro', **state)

    def jogo_campo_minado(self, user_id, form_data=None):
        state = self.game_controller.campo_minado_route(user_id, form_data)
        return template('app/views/html/campo_minado', **state)

    def jogo_caca_niquel(self, user_id, form_data=None):
        state = self.game_controller.caca_niquel_route(user_id, form_data)
        return template('app/views/html/caca_niquel', **state)

    def jogo_jogo_da_velha(self, user_id, form_data=None):
        state = self.game_controller.jogo_da_velha_route(user_id, form_data)
        return template('app/views/html/jogo_da_velha', **state)

    def jogo_caca_emoji(self, user_id, form_data=None):
        state = self.game_controller.caca_emoji_route(user_id, form_data)
        return template('app/views/html/caca_emoji', **state)

    def jogo_clique_rapido(self, user_id, form_data=None):
        state = self.game_controller.clique_rapido_route(user_id, form_data)
        return template('app/views/html/clique_rapido', **state)

    def jogo_mini_blackjack(self, user_id, form_data=None):
        state = self.game_controller.blackjack_route(user_id, form_data)
        return template('app/views/html/mini_black_jack', **state)

    def jogo_pedra_papel_tesoura(self, user_id, form_data=None):
        state = self.game_controller.ppt_route(user_id, form_data)
        return template('app/views/html/pedra_papel_tesoura', **state)

    def jogo_numero_secreto(self, user_id, form_data=None):
        state = self.game_controller.numero_secreto_route(user_id, form_data)
        return template('app/views/html/numero_secreto', **state)
