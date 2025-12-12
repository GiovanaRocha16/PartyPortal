import random
import time
import json
from app.controllers.player_controller import PlayerController
from app.controllers.user_controller import UserController
from app.controllers.websocket_manager import ws_manager


user_ctrl = UserController()

class GameController:
    """
    Controller responsável por operações e lógica de jogos
    """
    def __init__(self):
        self.players = PlayerController()
        self.clicks_data = {"count":0, "start":0}

 # ---------------------- PARTE ROUTE DOS JOGOS --------------------------        

    def confeiteiro_route(self, user_id, form_data):
        if not form_data:
            return {"resultado": None}
        ing1 = form_data.get('ing1')
        ing2 = form_data.get('ing2')
        ing3 = form_data.get('ing3')
        return self.confeiteiro(user_id, ing1, ing2, ing3)

    def campo_minado_route(self, user_id, form_data):
        if not form_data:
            return {
                "resultado": None,
                "clicados": [],
                "bomba": random.randint(1,9),
                "acabou": False
            }
        escolha = int(form_data.get('escolha'))
        clicados = [int(c) for c in form_data.get('clicados','').split(',') if c]
        bomba = int(form_data.get('bomba'))
        return self.campo_minado(user_id, escolha, clicados, bomba)

    def caca_niquel_route(self, user_id, form_data):
        return self.caca_niquel(user_id)

    def ppt_route(self, user_id, form_data):
        if not form_data:
            return {"escolha": None, "bot": None, "resultado": None}
        escolha = form_data.get('escolha')
        return self.pedra_papel_tesoura(user_id, escolha)

    def blackjack_route(self, user_id, form_data):
        if not form_data: 
            return self.mini_blackjack_inicial()
        acao = form_data.get('acao')
        jogador = json.loads(form_data.get('jogador'))
        bot = json.loads(form_data.get('bot'))
        return self.mini_blackjack_jogar(user_id, acao, jogador, bot)

    def jogo_da_velha_route(self, user_id, form_data):
        if not form_data:
            return {"tabuleiro": ["-"]*9, "mensagem": "Sua vez! Você é o X"}
        tabuleiro = form_data.get('tabuleiro').split(",")
        jogada = int(form_data.get('jogada'))
        return self.jogo_da_velha(user_id, tabuleiro, jogada)

    def caca_emoji_route(self, user_id, form_data):
        if not form_data:
            alvo_idx = random.randint(0,11)
            return {"opcoes": ["🟩"]*12, "alvo_idx": alvo_idx, "erros": 0, "mensagem":"Encontre o círculo verde!", "fim": False}
        escolha_idx = int(form_data.get('escolha_idx'))
        alvo_idx = int(form_data.get('alvo_idx'))
        erros = int(form_data.get('erros'))
        return self.caca_emoji(user_id, escolha_idx, alvo_idx, erros)

    def numero_secreto_route(self, user_id, form_data):
        if not form_data:
            return {"numero": random.randint(1,50), "tentativas":0, "mensagem":"Tente adivinhar!", "fim":False}
        numero = int(form_data.get('numero'))
        tentativas = int(form_data.get('tentativas'))
        chute = int(form_data.get('chute'))
        return self.numero_secreto(user_id, numero, tentativas, chute)

    def clique_rapido_route(self, user_id, form_data):
        if not form_data:
            return {"tempo": None, "cliques": self.clicks_data["count"]}
        if form_data.get("reset"):
            return self.clique_rapido(user_id, reset=True)
        if form_data.get("click"):
            return self.clique_rapido(user_id, click=True)
        return {"tempo": None, "cliques": self.clicks_data["count"]}

    # ---------------------- CONFEITEIRO --------------------------
    def confeiteiro(self, user_id, ing1, ing2, ing3):
        receitas = {
            ('Chocolate', 'Morango', 'Leite'): "Um bolo de morango delicioso! 🍰",
            ('Limão', 'Leite', 'Morango'): "Um mousse cítrico refrescante! 🍋🍓",
            ('Pimenta', 'Alho', 'Limão'): "🤢 Uma torta explosiva de alho e pimenta!",
            ('Chocolate', 'Leite', 'Pimenta'): "🔥 Um chocolate picante ousado!",
        }

        chave = (ing1, ing2, ing3)
        resultado = receitas.get(chave, f"🍽️ Uma criação misteriosa de {ing1}, {ing2} e {ing3}!")

        if "🤢" not in resultado and user_id:
            # premiação fixa: 5 pontos
            self.players.add_score_by_user_id(user_id, 5, websocket_manager=ws_manager, user_ctrl=user_ctrl)

        return {"resultado": resultado}

    # ---------------------- CAMPO MINADO --------------------------
    def campo_minado(self, user_id, escolha, clicados, bomba):
        if escolha not in clicados:
            clicados.append(escolha)

        if escolha == bomba:
            resultado = "💥 BOOM! Você pisou na bomba!"
            acabou = True

        elif len(clicados) == 8:
            resultado = "🏆 Parabéns! Você venceu sem explodir!"
            acabou = True

            if user_id:
                self.players.add_score_by_user_id(user_id, 10, websocket_manager=ws_manager, user_ctrl=user_ctrl)

        else:
            resultado = f"✅ {len(clicados)} tentativas seguras!"
            acabou = False

        return {
            "resultado": resultado,
            "clicados": clicados,
            "bomba": bomba,
            "acabou": acabou
        }

    # ---------------------- CAÇA-NÍQUEL --------------------------
    def caca_niquel(self, user_id):
        reels = ["🍒", "🍋", "🔔", "🍉", "⭐", "7️⃣"]
        slots = [random.choice(reels) for _ in range(3)]
        if slots[0] == slots[1] == slots[2]:
            if user_id:
                self.players.add_score_by_user_id(user_id, 5, websocket_manager=ws_manager, user_ctrl=user_ctrl)
            resultado = f"🏆 Parabéns! Você ganhou: {' '.join(slots)}"
        else:
            resultado = f"😢 Tente de novo: {' '.join(slots)}"
        return {"slots": slots, "resultado": resultado}

    # ---------------------- PEDRA PAPEL TESOURA --------------------------
    def pedra_papel_tesoura(self, user_id, escolha):
        opcoes = ["Pedra", "Papel", "Tesoura"]
        bot = random.choice(opcoes)

        if escolha == bot:
            resultado = "🤝 Empate!"
        elif (escolha == "Pedra" and bot == "Tesoura") or \
             (escolha == "Tesoura" and bot == "Papel") or \
             (escolha == "Papel" and bot == "Pedra"):
            resultado = "🎉 Você ganhou!"
            if user_id:
                self.players.add_score_by_user_id(user_id, 5, websocket_manager=ws_manager, user_ctrl=user_ctrl)
        else:
            resultado = "😢 Você perdeu!"

        return {"escolha": escolha, "bot": bot, "resultado": resultado}

    # ---------------------- MINI BLACKJACK --------------------------
    def mini_blackjack_inicial(self):
        cartas = list(range(1,11))
        jogador = [random.choice(cartas), random.choice(cartas)]
        bot = [random.choice(cartas), random.choice(cartas)]
        return {"jogador": jogador, "bot": bot, "fim": False}

    def mini_blackjack_jogar(self, user_id, acao, jogador, bot):
        cartas = list(range(1,11))
        if acao == "comprar":
            jogador.append(random.choice(cartas))
            if sum(jogador) > 21:
                return {"jogador": jogador, "bot": bot, "fim": True, "resultado": "💥 Você estourou! Derrota!"}
            return {"jogador": jogador, "bot": bot, "fim": False}

        if acao == "parar":
            while sum(bot) < 17:
                bot.append(random.choice(cartas))

            soma_j = sum(jogador)
            soma_b = sum(bot)

            if soma_b > 21:
                resultado = "🎉 O bot estourou! Você venceu!"
                if user_id:
                    self.players.add_score_by_user_id(user_id, 10, websocket_manager=ws_manager, user_ctrl=user_ctrl)
            elif soma_j > soma_b:
                resultado = "🎉 Você venceu!"
                if user_id:
                    self.players.add_score_by_user_id(user_id, 10, websocket_manager=ws_manager, user_ctrl=user_ctrl)
            elif soma_j < soma_b:
                resultado = "😢 Você perdeu!"
            else:
                resultado = "🤝 Empate!"

            return {"jogador": jogador, "bot": bot, "fim": True, "resultado": resultado}

    # ---------------------- JOGO DA VELHA --------------------------
    def jogo_da_velha(self, user_id, tabuleiro, jogada):
        if tabuleiro[jogada] != "-":
            return {"tabuleiro": tabuleiro, "mensagem": "Escolha uma casa vazia!"}

        tabuleiro[jogada] = "X"
        vitorias = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

        for a,b,c in vitorias:
            if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == "X":
                if user_id:
                    self.players.add_score_by_user_id(user_id, 10, websocket_manager=ws_manager, user_ctrl=user_ctrl)
                return {"tabuleiro": tabuleiro, "mensagem": "🎉 Você venceu!"}

        livres = [i for i,t in enumerate(tabuleiro) if t == "-"]
        if not livres:
            return {"tabuleiro": tabuleiro, "mensagem": "🤝 Empate!"}

        bot_joga = random.choice(livres)
        tabuleiro[bot_joga] = "O"

        for a,b,c in vitorias:
            if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == "O":
                return {"tabuleiro": tabuleiro, "mensagem": "😢 O bot venceu!"}

        return {"tabuleiro": tabuleiro, "mensagem": "Sua vez! Você é o X"}

    # ---------------------- CAÇA EMOJI --------------------------
    def caca_emoji(self, user_id, escolha_idx, alvo_idx, erros):
        alvo = "🟢"
        errado = "🟩"
        opcoes = [errado] * 12
        opcoes[alvo_idx] = alvo

        if escolha_idx == alvo_idx:
            if user_id:
                self.players.add_score_by_user_id(user_id, 10, websocket_manager=ws_manager, user_ctrl=user_ctrl)
            return {"opcoes": opcoes, "alvo_idx": alvo_idx, "erros": erros, "mensagem": "🎉 Você encontrou o emoji escondido!", "fim": True}

        erros += 1
        if erros >= 3:
            return {"opcoes": opcoes, "alvo_idx": alvo_idx, "erros": erros, "mensagem": "❌ Você errou 3 vezes! Fim de jogo!", "fim": True}

        return {"opcoes": opcoes, "alvo_idx": alvo_idx, "erros": erros, "mensagem": f"❌ Não é esse! ({erros}/3 erros)", "fim": False}

    # ---------------------- NÚMERO SECRETO --------------------------
    def numero_secreto(self, user_id, numero, tentativas, chute):
        tentativas += 1
        if chute == numero:
            if user_id:
                self.players.add_score_by_user_id(user_id, 15, websocket_manager=ws_manager, user_ctrl=user_ctrl)
            return {"numero": numero, "tentativas": tentativas, "mensagem": f"🎉 Acertou! O número era {numero}.", "fim": True}

        if chute < numero:
            msg = "🔼 O número secreto é MAIOR!"
        else:
            msg = "🔽 O número secreto é MENOR!"
        return {"numero": numero, "tentativas": tentativas, "mensagem": msg, "fim": False}

    # ---------------------- CLIQUE RÁPIDO --------------------------
    def clique_rapido(self, user_id, click=False, reset=False):
        if not hasattr(self, "clicks_data"):
            self.clicks_data = {"count":0, "start":0}

        if reset:
            self.clicks_data = {"count":0, "start":0}
            return {"tempo": None, "cliques": 0}

        if click:
            if self.clicks_data["count"] == 0:
                self.clicks_data["start"] = time.time()
            self.clicks_data["count"] += 1
            if self.clicks_data["count"] >= 10:
                total = round(time.time() - self.clicks_data["start"], 2)
                self.clicks_data = {"count":0, "start":0}
                if user_id:
                    self.players.add_score_by_user_id(user_id, 15, websocket_manager=ws_manager, user_ctrl=user_ctrl)
                return {"tempo": total, "cliques": 0}

        return {"tempo": None, "cliques": self.clicks_data["count"]}

