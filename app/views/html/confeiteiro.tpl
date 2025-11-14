<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🧁 Confeiteiro Maluco</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>🧁 Confeiteiro Maluco</h1>
        <p>Escolha 3 ingredientes e descubra sua criação!</p>
    </header>

    <main style="text-align:center;">
        <form method="post">
            <label>🍫 Ingrediente 1:</label>
            <select name="ing1">
                <option>Chocolate</option>
                <option>Morango</option>
                <option>Leite</option>
                <option>Limão</option>
                <option>Pimenta</option>
                <option>Alho</option>
            </select><br><br>

            <label>🍓 Ingrediente 2:</label>
            <select name="ing2">
                <option>Chocolate</option>
                <option>Morango</option>
                <option>Leite</option>
                <option>Limão</option>
                <option>Pimenta</option>
                <option>Alho</option>
            </select><br><br>

            <label>🥛 Ingrediente 3:</label>
            <select name="ing3">
                <option>Chocolate</option>
                <option>Morango</option>
                <option>Leite</option>
                <option>Limão</option>
                <option>Pimenta</option>
                <option>Alho</option>
            </select><br><br>

            <button type="submit">🍴 Misturar!</button>
        </form>

        % if resultado:
            <h2 style="margin-top:30px;">Resultado: {{resultado}}</h2>
        % end

        <br><br>
        <a href="/" 
           style="
            display:inline-block;
            background-color:#6a1b9a;
            color:white;
            padding:12px 24px;
            border-radius:12px;
            text-decoration:none;
            font-weight:bold;
            box-shadow:0 4px #4a116e;
            transition:all 0.2s ease;
           "
           onmouseover="this.style.backgroundColor='#7b1fa2'; this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px #4a116e';"
           onmouseout="this.style.backgroundColor='#6a1b9a'; this.style.transform='translateY(0)'; this.style.boxShadow='0 4px #4a116e';"
        >
           ⬅️ Voltar ao Menu
        </a>


    </main>
</body>
</html>
