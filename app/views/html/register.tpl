<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrar • Party Portal 🎉</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>

<body>
    <header>
        <h1>🎉 Party Portal 🎮</h1>
        <p>Crie sua conta e comece a jogar!</p>
    </header>

    <main class="form-container">
        <div class="form-card">
            <h2>Criar Conta</h2>
            % if erro:
                <p class="erro">{{erro}}</p>
            % end

            <form action="/register" method="POST">
                <input type="text" name="username" placeholder="Usuário" required>
                <input type="password" name="password" placeholder="Senha" required>
                <button type="submit">Registrar</button>
            </form>

            <a href="/login" class="form-link">Já tem conta? Fazer login</a>
        </div>
    </main>

    <footer style="position: fixed; bottom: 0; left: 0; width: 100%;"> 
        <p>© 2025 Party Portal — Projeto BMVC I</p>
    </footer>
</body>
</html>
