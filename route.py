# route.py (refatorado BMVC/POO, lógica completa mantida)
from bottle import Bottle, request, static_file, redirect, template, response, BaseRequest, run
from app.controllers.application import Application
from app.controllers.user_controller import UserController
from app.controllers.player_controller import PlayerController
from app.controllers.game_controller import GameController
from app.controllers.session_manager import SessionManager

BaseRequest.MEMFILE_MAX = 1024 * 1024

# -------------------- APP & CONTROLLERS --------------------
app = Bottle()
ctl = Application()
user_ctrl = UserController()
player_ctrl = PlayerController()
game_ctrl = GameController()
session_ctrl = SessionManager()

# -------------------- STATIC FILES --------------------
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

# -------------------- HOME --------------------
@app.route('/')
@app.route('/home')
def home():
    user = ctl.current_user()
    if not user:
        redirect("/login")
    return ctl.render('home')

# -------------------- LOGIN / REGISTER --------------------
@app.route('/login')
def login_view():
    return template('app/views/html/login', erro=None)

@app.post('/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = user_ctrl.login(username, password)
    if result.get("error"):
        return template('app/views/html/login', erro=result["error"])

    user = result["user"]
    sid = session_ctrl.create_session(user)
    response.set_cookie("session_id", sid, path="/")
    redirect(result.get("redirect", "/home"))

@app.route('/logout')
def logout():
    ctl.logout_user()
    redirect('/login')

@app.route('/register')
def register_view():
    return template('app/views/html/register', erro=None)

@app.post('/register')
def register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not username or not password:
        return template('app/views/html/register', erro="Usuário e senha são obrigatórios")

    result = user_ctrl.register({"username": username, "password": password})
    if result.get("error"):
        return template('app/views/html/register', erro=result["error"])
    redirect('/login')

# -------------------- PLAYERS --------------------
@app.route('/players')
def list_players():
    user = ctl.current_user()
    if not user:
        redirect("/login")
    players = player_ctrl.list_players()
    return template('app/views/html/players', players=players)

@app.post('/players/add')
def add_player():
    user = ctl.current_user()
    if not user:
        redirect("/login")
    player_ctrl.create_player_for_user(user["id"], f"Player{user['id']}")
    redirect('/players')

@app.post('/players/update')
def update_player():
    user = ctl.current_user()
    if not user:
        redirect("/login")
    player_id = int(request.forms.get('id'))
    score = int(request.forms.get('score') or 0)
    player_ctrl.update_score(player_id, score)
    redirect('/players')

@app.post('/players/delete')
def delete_player():
    user = ctl.current_user()
    if not user:
        redirect("/login")
    player_id = int(request.forms.get('id'))
    player_ctrl.delete_player(player_id)
    redirect('/players')

# -------------------- ADMIN --------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    usuarios = user_ctrl.list_users()
    players = player_ctrl.list_players()
    return template('app/views/html/admin_dashboard', usuarios=usuarios, players=players)

@app.post('/admin/user/add')
def admin_add_user():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = user_ctrl.register({"username": username, "password": password})
    if result.get("error"):
        usuarios = user_ctrl.list_users()
        players = player_ctrl.list_players()
        return template("app/views/html/admin_dashboard", usuarios=usuarios, players=players, erro=result["error"])
    redirect('/admin/dashboard')

@app.post('/admin/user/update')
def admin_update_user():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    user_id = int(request.forms.get('id'))
    username = request.forms.get('username')
    password = request.forms.get('password')
    user_ctrl.update_user(user_id, username, password)
    redirect('/admin/dashboard')

@app.post('/admin/user/delete')
def admin_delete_user():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    user_id = int(request.forms.get('id'))
    user_ctrl.delete_user(user_id)
    player_ctrl.delete_player_by_user_id(user_id)
    redirect('/admin/dashboard')

@app.route('/admin/sessions')
def admin_sessions():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    sessions = session_ctrl.list_sessions()
    return template('app/views/html/admin_sessions', sessions=sessions)

@app.post('/admin/session/delete')
def admin_delete_session():
    if not ctl.check_permission(admin_required=True):
        return ctl.access_denied()
    session_id = request.forms.get('session_id')
    session_ctrl.delete_session(session_id)
    redirect('/admin/dashboard')

# -------------------- GAMES --------------------
def handle_game_route(route_func, template_name):
    user_id = ctl.get_user_id()
    state = route_func(user_id, request.forms)
    return template(template_name, **state)

@app.route('/confeiteiro', method=['GET','POST'])
def confeiteiro():
    return handle_game_route(game_ctrl.confeiteiro_route, 'app/views/html/confeiteiro')

@app.route('/campo_minado', method=['GET','POST'])
def campo_minado():
    return handle_game_route(game_ctrl.campo_minado_route, 'app/views/html/campo_minado')

@app.route('/caca_niquel', method=['GET','POST'])
def caca_niquel():
    return handle_game_route(game_ctrl.caca_niquel_route, 'app/views/html/caca_niquel')

@app.route('/pedra_papel_tesoura', method=['GET','POST'])
def ppt():
    return handle_game_route(game_ctrl.ppt_route, 'app/views/html/pedra_papel_tesoura')

@app.route('/mini_black_jack', method=['GET','POST'])
def blackjack():
    return handle_game_route(game_ctrl.blackjack_route, 'app/views/html/mini_black_jack')

@app.route('/jogo_da_velha', method=['GET','POST'])
def jogo_da_velha():
    return handle_game_route(game_ctrl.jogo_da_velha_route, 'app/views/html/jogo_da_velha')

@app.route('/caca_emoji', method=['GET','POST'])
def caca_emoji():
    return handle_game_route(game_ctrl.caca_emoji_route, 'app/views/html/caca_emoji')

@app.route('/numero_secreto', method=['GET','POST'])
def numero_secreto():
    return handle_game_route(game_ctrl.numero_secreto_route, 'app/views/html/numero_secreto')

@app.route('/clique_rapido', method=['GET','POST'])
def clique_rapido():
    return handle_game_route(game_ctrl.clique_rapido_route, 'app/views/html/clique_rapido')

# -------------------- RUN --------------------
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
