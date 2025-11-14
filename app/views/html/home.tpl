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
        <p>Escolha seu mini-jogo e divirta-se!</p>
    </header>

<body>
    <header>
        <p>Esse site é o nosso trabalho do BMVC. Tem como objetivo ser um ambiente com vários mini-jogos divertidos para desestressar! Esperamos que gostem! 
        Para esse primeiro nível fizemos a página estática principal com todos os jogos. No futuro, pretendemos adicionar sistema de recorde e login com banco de dados, além, é claro, dos jogos (em python)! </p>
    </header>

    <main class="games-container">
        <div class="game-card">
            <h2>🎯 Clique Rápido</h2>
            <p>Clique o máximo de alvos que conseguir em 10 segundos!</p>
            <button onclick="iniciarJogo('Clique Rápido')">Jogar</button>
        </div>

        <div class="game-card">
            <h2>💭 Número Secreto</h2>
            <p>Adivinhe o número misterioso com dicas “maior” ou “menor”.</p>
            <button onclick="iniciarJogo('Número Secreto')">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🧠 Jogo da Velha</h2>
            <p>Clássico! Vença o computador ou desafie um amigo.</p>
            <button onclick="iniciarJogo('Jogo da Velha')">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🐸 Caça ao Emoji</h2>
            <p>Encontre o emoji certo entre vários que aparecem!</p>
            <button onclick="iniciarJogo('Caça ao Emoji')">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🃏 Mini Blackjack</h2>
            <p>Tente chegar o mais perto possível do 21!</p>
            <button onclick="iniciarJogo('Mini Blackjack')">Jogar</button>
        </div>
        
        <div class="game-card">
            <h2>✂️ Pedra, Papel e Tesoura</h2>
            <p>Escolha entre pedra, papel e tesoura e veja se ganhou!</p>
            <button onclick="iniciarJogo('Pedra, Papel e Tesoura')">Jogar</button>
        </div>

        <div class="game-card">
            <h2>🎰 Caça-Níquel</h2>
            <p>Puxe a alavanca para jogar e teste sua sorte!</p>
            <button onclick="iniciarJogo('Caça-Níquel')">Jogar</button>
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
