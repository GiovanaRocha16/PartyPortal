<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🐸 Caça ao Emoji</title>

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);
            text-align: center;
            padding: 40px;
            color: white;
        }

        h1 {
            font-size: 34px;
            margin-bottom: 20px;
        }

        .emoji-grid {
            display: grid;
            grid-template-columns: repeat(4, 70px);
            gap: 20px;
            justify-content: center;
            margin-top: 25px;
        }

        .emoji-btn {
            background-color: #6a1b9a;
            color: white;
            padding: 15px;
            font-size: 30px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
            transition: 0.15s ease-in-out;
        }

        .emoji-btn:hover {
            transform: scale(1.1);
        }

        .emoji-btn:active {
            transform: scale(1);
            box-shadow: none;
        }

        .resultado {
            margin-top: 30px;
            font-size: 24px;
            font-weight: bold;
        }

        /* botão jogar novamente */
        .btn-jogar {
            background-color: #6a1b9a;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
            margin-top: 25px;
        }

        .btn-jogar:hover {
            transform: scale(1.05);
        }

        /* botão voltar */
        .btn-voltar {
            display: inline-block;
            background-color: #6a1b9a;
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px #4a0d6e;
            margin-top: 40px;
        }
    </style>
</head>

<body>

    <h1>🐸 Caça ao Emoji</h1>

    <div class="resultado">{{mensagem}}</div>

    % if not fim:
        <div class="emoji-grid">
            % for i in range(len(opcoes)):
                % e = opcoes[i]
                <form method="POST" style="display:inline-block;">
                    <input type="hidden" name="alvo_idx" value="{{alvo_idx}}">
                    <input type="hidden" name="erros" value="{{erros}}">
                    <button class="emoji-btn" name="escolha_idx" value="{{i}}">{{e}}</button>
                </form>
            % end
        </div>

        <div class="resultado">
            Erros: <b>{{erros}}</b> / 3
        </div>

    % else:
        <form method="GET">
            <button class="btn-jogar">🔁 Jogar Novamente</button>
        </form>
    % end

    <a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

</body>
</html>
