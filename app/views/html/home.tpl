<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Party Portal 🎉</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <script src="/static/js/script.js" defer></script>
</head>
<body>
    <header>
        <h1>🎉 Party Portal 🎮</h1>

        % if username:
            <div class="user-info">
                <p>
                    Bem-vindo, <strong>{{ username }}</strong>! |
                    Pontuação: <strong>{{ user_score if user_score is not None else 0 }}</strong> |
                    Posição: <strong>{{ user_position if user_position is not None else '-' }}</strong>
                </p>

                <div class="header-actions">
                    <button onclick="window.location.href='/ranking'">Ranking 🏆</button>
                    <button onclick="window.location.href='/logout'">Logout</button>
                </div>
            </div>
        % else:
            <p>Escolha seu mini-jogo e divirta-se!</p>
        % end
    </header>

    <main class="games-container">
        <div class="game-card">
            <h2>🎯 Clique Rápido</h2>
            <p>Clique o máximo de alvos que conseguir em 10 segundos!</p>
            <button onclick="window.location.href='/clique_rapido'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>💭 Número Secreto</h2>
            <p>Adivinhe o número misterioso com dicas “maior” ou “menor”.</p>
            <button onclick="window.location.href='/numero_secreto'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🧠 Jogo da Velha</h2>
            <p>Clássico! Vença o computador e prove ser o melhor!</p>
            <button onclick="window.location.href='/jogo_da_velha'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🐸 Caça ao Emoji</h2>
            <p>Encontre o emoji certo entre vários que aparecem!</p>
            <button onclick="window.location.href='/caca_emoji'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🃏 Mini Blackjack</h2>
            <p>Tente chegar o mais perto possível do 21!</p>
            <button onclick="window.location.href='/mini_black_jack'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>✂️ Pedra, Papel e Tesoura</h2>
            <p>Escolha entre pedra, papel e tesoura e veja se ganhou!</p>
            <button onclick="window.location.href='/pedra_papel_tesoura'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🎰 Caça-Níquel</h2>
            <p>Puxe a alavanca para jogar e teste sua sorte!</p>
            <button onclick="window.location.href='/caca_niquel'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>💣 Mini Campo Minado</h2>
            <p>Tente não acertar as bombas para sobreviver!</p>
            <button onclick="window.location.href='/campo_minado'">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🧁 Confeiteiro Maluco</h2>
            <p>Escolha 3 ingredientes e descubra sua criação maluca!</p>
            <button onclick="window.location.href='/confeiteiro'">Jogar</button>
        </div>
    </main>

    <footer>
        <p>© 2025 Party Portal — Projeto BMVC I</p>
    </footer>
</body>
</html>
