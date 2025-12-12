<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Ranking – Party Portal</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <!-- carrega apenas o websocket.js nesta página -->
    <script src="/static/js/websocket.js" defer></script>
    <style>
        body {
            background: #111;
            color: #fff;
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 { text-align: center; }
        #ranking {
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            background: #222;
            border-radius: 10px;
        }
        .item {
            padding: 10px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
        }
        .item:last-child { border-bottom: none; }
        .back-btn {
            margin: 20px auto;
            display: block;
            padding: 10px 20px;
            background: #444;
            color: #fff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>

<h1>🏆 Ranking</h1>

<div id="ranking">
    <p>Carregando ranking...</p>
</div>

<button class="back-btn" onclick="window.location.href='/'">Voltar</button>

</body>
</html>
