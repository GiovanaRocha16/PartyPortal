<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🧠 Jogo da Velha</title>

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);
            color: white;
            text-align: center;
            padding: 30px;
        }

        h1 { font-size: 36px; margin-bottom: 15px; }

        .tabuleiro {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            gap: 10px;
            justify-content: center;
            margin-top: 30px;
        }

        .casa {
            width: 100px;
            height: 100px;
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            font-size: 48px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: 0.2s;
        }

        .casa:hover {
            transform: scale(1.05);
            background: rgba(255,255,255,0.25);
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
            margin-top: 25px;
        }

        .btn:hover { transform: scale(1.05); }

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

<h1>🧠 Jogo da Velha</h1>

<h2>{{mensagem}}</h2>

<div class="tabuleiro">
% for i in range(9):
    <form method="POST">
        <input type="hidden" name="tabuleiro" value="{{','.join(tabuleiro)}}">

        <button class="casa" name="jogada" value="{{i}}">
            {{ tabuleiro[i] if tabuleiro[i] != '-' else '' }}
        </button>
    </form>
% end
</div>

<form method="GET">
    <button class="btn">🔁 Reiniciar</button>
</form>

<a class="btn-voltar" href="/">⬅️ Voltar ao Menu</a>

</body>
</html>
