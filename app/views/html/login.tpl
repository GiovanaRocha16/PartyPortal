<!-- Login Page -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login • Party Portal 🎉</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>🎉 Party Portal 🎮</h1>
        <p>Faça login para acessar os mini-jogos!</p>
    </header>

    <main class="form-container">
        <div class="form-card">
            <h2>Entrar</h2>
            % if erro:
                <p style="color: #ff8080; font-weight: bold;">{{erro}}</p>
            % end

            % if defined('sucesso') and sucesso:
                <p style="color: #80ff80; font-weight: bold;">{{sucesso}}</p>
            % end
            <form action="/login" method="POST">
                <input type="text" name="username" placeholder="Usuário" required>
                <input type="password" name="password" placeholder="Senha" required>
                <button type="submit">Login</button>
            </form>
            <a href="/register" class="form-link">Criar conta</a>
        </div>
    </main>

    <footer style="position: fixed; bottom: 0; left: 0; width: 100%;"> 
        <p>© 2025 Party Portal — Projeto BMVC I</p>
    </footer>
</body>
</html>
