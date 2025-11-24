<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>✊🖐✌ Pedra, Papel e Tesoura</title>

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

        .opcoes {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-top: 30px;
        }

        .btn-opcao {
            background-color: #6a1b9a;
            color: white;
            padding: 15px 25px;
            font-size: 22px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
        }

        .btn-opcao:active {
            transform: translateY(3px);
            box-shadow: none;
        }

        .resultado {
            margin-top: 30px;
            font-size: 26px;
            font-weight: bold;
        }

        .btn-jogar {
            background: #6a1b9a;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
            margin-top: 20px;
            transition: 0.15s ease-in-out;
        }

        .btn-jogar:hover {
            transform: scale(1.05);
        }

        .btn-jogar:active {
            transform: scale(1);
            box-shadow: none;
        }


        /* botão de voltar */
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

    <h1>✊🖐✌ Pedra, Papel e Tesoura</h1>

    % if escolha:
        <div class="resultado">
            Você escolheu: <b>{{escolha}}</b><br>
            O computador escolheu: <b>{{bot}}</b><br><br>
            <span>{{resultado}}</span>
        </div>

        <br>
        <form method="POST">
            <button class="btn-jogar" name="escolha" value="">🔁 Jogar Novamente</button>
        </form>
    % else:
        <h2>Escolha uma opção:</h2>

        <div class="opcoes">
            <form method="POST">
                <button class="btn-opcao" name="escolha" value="Pedra">✊ Pedra</button>
            </form>

            <form method="POST">
                <button class="btn-opcao" name="escolha" value="Papel">🖐 Papel</button>
            </form>

            <form method="POST">
                <button class="btn-opcao" name="escolha" value="Tesoura">✌ Tesoura</button>
            </form>
        </div>
    % end

    <!-- botão voltar -->
    <a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

</body>
</html>
