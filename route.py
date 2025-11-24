from app.models.player import Player
from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response
import random
import json
import time

app = Bottle()
ctl = Application()

@app.route('/players')
def list_players():
    return template('app/views/html/players', players=Player.all())

@app.post('/players/add')
def add_player():
    name = request.forms.get('name')
    Player.create(name)
    redirect('/players')

@app.post('/players/update')
def update_player():
    player_id = int(request.forms.get('id'))
    name = request.forms.get('name')
    score = int(request.forms.get('score') or 0)
    Player.update(player_id, name, score)
    redirect('/players')

@app.post('/players/delete')
def delete_player():
    player_id = int(request.forms.get('id'))
    Player.delete(player_id)
    redirect('/players')

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/')
def action_home(info=None):
    return ctl.render('home')


@app.route('/confeiteiro', method=['GET', 'POST'])
def confeiteiro():
    if request.method == 'POST':
        ing1 = request.forms.get('ing1')
        ing2 = request.forms.get('ing2')
        ing3 = request.forms.get('ing3')
        nome_jogador = request.forms.get('nome_jogador')

        receitas = {
            ('Chocolate', 'Morango', 'Leite'): "Um bolo de morango delicioso! 🍰",
            ('Limão', 'Leite', 'Morango'): "Um mousse cítrico refrescante! 🍋🍓",
            ('Pimenta', 'Alho', 'Limão'): "🤢 Uma torta explosiva de alho e pimenta!",
            ('Chocolate', 'Leite', 'Pimenta'): "🔥 Um chocolate picante ousado!",
        }

        chave = (ing1, ing2, ing3)
        resultado = receitas.get(chave, f"🍽️ Uma criação misteriosa de {ing1}, {ing2} e {ing3}!")

        if "🤢" not in resultado and nome_jogador:
            Player.create(nome_jogador, score=5)

        return template('app/views/html/confeiteiro', resultado=resultado)
    else:
        return template('app/views/html/confeiteiro', resultado=None)

@app.route('/campo_minado', method=['GET', 'POST'])
def campo_minado():
    bomba = random.randint(1, 9)
    resultado = None
    clicados = []

    if request.method == 'POST':
        escolha = int(request.forms.get('escolha'))
        clicados = request.forms.get('clicados', '')
        clicados = [int(c) for c in clicados.split(',') if c]
        nome_jogador = request.forms.get("nome_jogador")

        if escolha not in clicados:
            clicados.append(escolha)

        if escolha == bomba:
            resultado = f"💥 BOOM! Você pisou na bomba!"
        elif len(clicados) == 8:
            resultado = "🏆 Parabéns! Você venceu sem explodir!"
            if nome_jogador:
                Player.create(nome_jogador, score=10)
        else:
            resultado = f"✅ {len(clicados)} tentativas seguras!"

    return template('app/views/html/campo_minado',
                    resultado=resultado,
                    clicados=clicados,
                    bomba=bomba)

@app.route('/caça_níquel', method=['GET', 'POST'])
def caça_níquel():
    resultado = None
    reels = ["🍒", "🍋", "🔔", "🍉", "⭐", "7️⃣"]
    slots = ["❓", "❓", "❓"]

    if request.method == 'POST':
        slots = [random.choice(reels) for _ in range(3)]
        nome_jogador = request.forms.get("nome_jogador")
        if slots[0] == slots[1] == slots[2]:
            resultado = f"🏆 Parabéns! Você ganhou: {' '.join(slots)}"
            if nome_jogador:
                Player.create(nome_jogador, score=5)
        else:
            resultado = f"😢 Tente de novo: {' '.join(slots)}"

    return template('app/views/html/caca_niquel', slots=slots, resultado=resultado)

@app.route('/pedra_papel_tesoura', method=['GET', 'POST'])
def pedra_papel_tesoura():
    if request.method == 'POST':
        escolha = request.forms.get('escolha')
        nome_jogador = request.forms.get("nome_jogador")
        opcoes = ["Pedra", "Papel", "Tesoura"]
        bot = random.choice(opcoes)

        if escolha == bot:
            resultado = "🤝 Empate!"
        elif (escolha == "Pedra" and bot == "Tesoura") or \
             (escolha == "Tesoura" and bot == "Papel") or \
             (escolha == "Papel" and bot == "Pedra"):
            resultado = "🎉 Você ganhou!"
            if nome_jogador:
                Player.create(nome_jogador, score=5)
        else:
            resultado = "😢 Você perdeu!"

        return template("app/views/html/pedra_papel_tesoura",
                        escolha=escolha, bot=bot, resultado=resultado)

    return template("app/views/html/pedra_papel_tesoura",
                    escolha=None, bot=None, resultado=None)

@app.route('/mini_black_jack', method=['GET', 'POST'])
def blackjack():
    cartas = [1,2,3,4,5,6,7,8,9,10]

    if request.method == 'GET':
        jogador = [random.choice(cartas), random.choice(cartas)]
        bot = [random.choice(cartas), random.choice(cartas)]
        return template("app/views/html/mini_black_jack",
                        jogador=jogador, bot=bot, fim=False)

    acao = request.forms.get("acao")
    jogador = json.loads(request.forms.get("jogador"))
    bot = json.loads(request.forms.get("bot"))
    nome_jogador = request.forms.get("nome_jogador")

    if acao == "comprar":
        jogador.append(random.choice(cartas))
        if sum(jogador) > 21:
            return template("app/views/html/mini_black_jack",
                            jogador=jogador,
                            bot=bot,
                            fim=True,
                            resultado="💥 Você estourou! Derrota!")
        return template("app/views/html/mini_black_jack",
                        jogador=jogador, bot=bot, fim=False)

    if acao == "parar":
        while sum(bot) < 17:
            bot.append(random.choice(cartas))

        soma_jog = sum(jogador)
        soma_bot = sum(bot)

        if soma_bot > 21:
            resultado = "🎉 O bot estourou! Você venceu!"
            if nome_jogador:
                Player.create(nome_jogador, score=10)
        elif soma_jog > soma_bot:
            resultado = "🎉 Você venceu!"
            if nome_jogador:
                Player.create(nome_jogador, score=10)
        elif soma_jog < soma_bot:
            resultado = "😢 Você perdeu!"
        else:
            resultado = "🤝 Empate!"

        return template("app/views/html/mini_black_jack",
                        jogador=jogador,
                        bot=bot,
                        fim=True,
                        resultado=resultado)

@app.route('/jogo_da_velha', method=['GET', 'POST'])
def jogo_da_velha():
    if request.method == 'GET':
        tabuleiro = ["-"] * 9
        return template("app/views/html/jogo_da_velha",
                        tabuleiro=tabuleiro,
                        mensagem="Sua vez! Você é o X")

    tabuleiro = request.forms.get("tabuleiro").split(",")
    jogada = int(request.forms.get("jogada"))
    nome_jogador = request.forms.get("nome_jogador")

    if tabuleiro[jogada] != "-":
        return template("app/views/html/jogo_da_velha",
                        tabuleiro=tabuleiro,
                        mensagem="Escolha uma casa vazia!")

    tabuleiro[jogada] = "X"
    vitorias = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    for a,b,c in vitorias:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == "X":
            if nome_jogador:
                Player.create(nome_jogador, score=10)
            return template("app/views/html/jogo_da_velha",
                            tabuleiro=tabuleiro,
                            mensagem="🎉 Você venceu!")

    livres = [i for i,t in enumerate(tabuleiro) if t == "-"]
    if not livres:
        return template("app/views/html/jogo_da_velha",
                        tabuleiro=tabuleiro,
                        mensagem="🤝 Empate!")

    bot_joga = random.choice(livres)
    tabuleiro[bot_joga] = "O"

    for a,b,c in vitorias:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == "O":
            return template("app/views/html/jogo_da_velha",
                            tabuleiro=tabuleiro,
                            mensagem="😢 O bot venceu!")

    return template("app/views/html/jogo_da_velha",
                    tabuleiro=tabuleiro,
                    mensagem="Sua vez! Você é o X")

@app.route('/caca_emoji', method=['GET', 'POST'])
def caca_emoji():
    if request.method == "GET":
        alvo = "🟢"
        errado = "🟩"
        erros = 0
        opcoes = [errado] * 12
        alvo_idx = random.randint(0, 11)
        opcoes[alvo_idx] = alvo
        return template("app/views/html/caca_emoji",
                        opcoes=opcoes,
                        alvo_idx=alvo_idx,
                        erros=erros,
                        mensagem="Encontre o círculo verde! 🟢",
                        fim=False)

    escolha_idx = int(request.forms.get("escolha_idx"))
    alvo_idx = int(request.forms.get("alvo_idx"))
    erros = int(request.forms.get("erros"))
    nome_jogador = request.forms.get("nome_jogador")

    alvo = "🟢"
    errado = "🟩"
    opcoes = [errado] * 12
    opcoes[alvo_idx] = alvo

    if escolha_idx == alvo_idx:
        if nome_jogador:
            Player.create(nome_jogador, score=10)
        return template("app/views/html/caca_emoji",
                        opcoes=opcoes,
                        alvo_idx=alvo_idx,
                        erros=erros,
                        mensagem="🎉 Você encontrou o emoji escondido!",
                        fim=True)

    erros += 1
    if erros >= 3:
        return template("app/views/html/caca_emoji",
                        opcoes=opcoes,
                        alvo_idx=alvo_idx,
                        erros=erros,
                        mensagem="❌ Você errou 3 vezes! Fim de jogo!",
                        fim=True)

    return template("app/views/html/caca_emoji",
                    opcoes=opcoes,
                    alvo_idx=alvo_idx,
                    erros=erros,
                    mensagem=f"❌ Não é esse! ({erros}/3 erros)",
                    fim=False)

@app.route('/numero_secreto', method=['GET', 'POST'])
def numero_secreto():
    if request.method == "GET":
        numero = random.randint(1, 50)
        tentativas = 0
        return template("app/views/html/numero_secreto",
                        numero=numero,
                        tentativas=tentativas,
                        mensagem="Tente adivinhar o número entre 1 e 50!",
                        fim=False)

    numero = int(request.forms.get("numero"))
    tentativas = int(request.forms.get("tentativas"))
    chute = int(request.forms.get("chute"))
    nome_jogador = request.forms.get("nome_jogador")

    tentativas += 1
    if chute == numero:
        if nome_jogador:
            Player.create(nome_jogador, score=15)
        return template("app/views/html/numero_secreto",
                        numero=numero,
                        tentativas=tentativas,
                        mensagem=f"🎉 Acertou! O número era {numero}.",
                        fim=True)
    elif chute < numero:
        msg = "🔼 O número secreto é MAIOR!"
    else:
        msg = "🔽 O número secreto é MENOR!"

    return template("app/views/html/numero_secreto",
                    numero=numero,
                    tentativas=tentativas,
                    mensagem=msg,
                    fim=False)

clicks_data = {"count": 0, "start": 0}

@app.route('/clique_rapido', method=['GET', 'POST'])
def clique_rapido():
    global clicks_data
    if request.method == 'GET':
        return template("app/views/html/clique_rapido",
                        tempo=None,
                        cliques=clicks_data["count"])

    nome_jogador = request.forms.get("nome_jogador")
    if request.forms.get("reset"):
        clicks_data = {"count": 0, "start": 0}
        return template("app/views/html/clique_rapido",
                        tempo=None,
                        cliques=0)

    if request.forms.get("click"):
        if clicks_data["count"] == 0:
            clicks_data["start"] = time.time()
        clicks_data["count"] += 1

        if clicks_data["count"] >= 10:
            total = round(time.time() - clicks_data["start"], 2)
            clicks_data = {"count": 0, "start": 0}
            if nome_jogador:
                Player.create(nome_jogador, score=15)
            return template("app/views/html/clique_rapido",
                            tempo=total,
                            cliques=0)

        return template("app/views/html/clique_rapido",
                        tempo=None,
                        cliques=clicks_data["count"])

    return template("app/views/html/clique_rapido",
                    tempo=None,
                    cliques=clicks_data["count"])

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
