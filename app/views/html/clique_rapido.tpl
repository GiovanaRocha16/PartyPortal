<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>⚡ Teste de Velocidade</title>

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

        .btn-opcao, .btn-jogar {
            background-color: #6a1b9a;
            color: white;
            padding: 15px 25px;
            font-size: 22px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px #4a0d6e;
            transition: 0.15s ease-in-out;
        }

        .btn-opcao:hover, .btn-jogar:hover {
            transform: scale(1.05);
        }

        .btn-opcao:active, .btn-jogar:active {
            transform: scale(1);
            box-shadow: none;
        }

        .resultado {
            margin-top: 30px;
            font-size: 26px;
            font-weight: bold;
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
            margin-top: 35px;
        }
    </style>
</head>

<body>

    <h1>⚡ Teste de Velocidade</h1>

    % if tempo is not None:
        <div class="resultado">
            Você clicou 10 vezes em:<br><br>
            <span><b>{{tempo}} segundos</b></span>
        </div>

        <br>
        <form method="POST">
            <button class="btn-jogar" name="reset" value="1">🔁 Tentar Novamente</button>
        </form>

    % else:
        <h2>Clique no botão abaixo 10 vezes!</h2>

        <form method="POST">
            <button class="btn-opcao" name="click" value="1">🖱️ Clique!</button>
        </form>

        <div class="resultado">
            Cliques: <b>{{cliques}}</b> / 10
        </div>
    % end

    <a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

</body>
</html>
