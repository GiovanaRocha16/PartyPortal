<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🔢 Número Secreto</title>

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #5ee7df, #b490ca);
            text-align: center;
            padding: 40px;
            color: white;
        }

        h1 { font-size: 34px; margin-bottom: 10px; }

        .box {
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 14px;
            width: 350px;
            margin: 20px auto;
        }

        input[type="number"] {
            font-size: 20px;
            padding: 8px;
            width: 120px;
            border-radius: 10px;
            border: none;
        }

        .btn {
            margin-top: 15px;
            background: #6a1b9a;
            padding: 10px 25px;
            color: white;
            font-size: 18px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
        }

        .btn:hover { transform: scale(1.05); }

        .btn-voltar {
            display: inline-block;
            margin-top: 25px;
            background: #6a1b9a;
            padding: 10px 20px;
            color: white;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px #4a0d6e;
        }
    </style>
</head>

<body>

<h1>💭 Número Secreto</h1>

<div class="box">
    <h2>{{mensagem}}</h2>
    <p>Tentativas: <b>{{tentativas}}</b></p>

% if not fim:
    <form method="POST">
        <input type="hidden" name="numero" value="{{numero}}">
        <input type="hidden" name="tentativas" value="{{tentativas}}">

        <input type="number" name="chute" min="1" max="50" required>
        <br>
        <button class="btn">Enviar</button>
    </form>
% else:
    <form method="GET">
        <button class="btn">🔁 Jogar Novamente</button>
    </form>
% end
</div>

<a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

</body>
</html>
