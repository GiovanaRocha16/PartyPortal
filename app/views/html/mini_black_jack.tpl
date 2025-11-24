% import json
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🃏 Mini Blackjack</title>

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);
            text-align: center;
            padding: 35px;
            color: white;
        }

        h1 {
            font-size: 34px;
            margin-bottom: 15px;
        }

        .cartas {
            font-size: 26px;
            margin: 10px 0;
        }

        .btn {
            background: #6a1b9a;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
            margin: 10px;
        }

        .btn:hover { transform: scale(1.05); }
        .btn:active { transform: scale(1); box-shadow: none; }

        .btn-voltar {
            display: inline-block;
            background-color: #6a1b9a;
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px #4a0d6e;
            margin-top: 35px;
        }
    </style>
</head>

<body>

<h1>🃏 Mini Blackjack</h1>

<div class="cartas">
    <b>Suas cartas:</b> {{jogador}} (total: {{sum(jogador)}})
</div>

<div class="cartas">
    <b>Cartas do bot:</b>
    % if fim:
        {{bot}} (total: {{sum(bot)}})
    % else:
        [? , {{bot[1]}}]
    % end
</div>

% if not fim:
    <form method="POST">

        <!-- Agora serialize corretamente -->
        <input type="hidden" name="jogador" value='{{!json.dumps(jogador)}}'>
        <input type="hidden" name="bot" value='{{!json.dumps(bot)}}'>

        <button class="btn" name="acao" value="comprar">➕ Comprar carta</button>
        <button class="btn" name="acao" value="parar">🛑 Parar</button>
    </form>
% else:
    <h2>{{resultado}}</h2>

    <form method="GET">
        <button class="btn">🔁 Jogar Novamente</button>
    </form>
% end

<a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

</body>
</html>
