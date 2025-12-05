<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <style>
        body { font-family: Arial; background:#f3f3f3; padding:30px; }
        h1 { text-align:center; margin-bottom:40px; }
        h2 { margin-top:40px; }
        table {
            width: 100%;
            background:white;
            border-collapse: collapse;
            margin-bottom:30px;
            box-shadow:0 0 5px rgba(0,0,0,0.2);
        }
        th, td { padding:10px; border-bottom:1px solid #ddd; text-align:left; }
        th { background:#222; color:white; }
        form { display:inline-block; margin:0 5px; }
        button {
            padding:5px 10px;
            cursor:pointer;
            background:#333;
            color:white;
            border:none;
            border-radius:4px;
        }
        button.delete { background:#b30000; }
        button.update { background:#0044aa; }
        button.add { background:#008000; }
        input[type="text"], input[type="password"] {
            padding:5px;
            margin-right:5px;
        }
    </style>
</head>
<body>

    <h1>📊 Painel Administrativo</h1>

    <!-- ============================ USERS ============================ -->
    <h2>🧑‍💻 Logins (Users)</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Ações</th>
        </tr>

        % for u in usuarios:
        <tr>
            <td>{{u[0]}}</td>

            <td>
                <!-- Form para editar usuário -->
                <form action="/admin/user/update" method="POST">
                    <input type="hidden" name="id" value="{{!u[0]}}">
                    <input type="text" name="username" value="{{!u[1]}}" required>
                    <input type="password" name="password" placeholder="Nova senha (opcional)">
                    <button type="submit" class="update">Salvar</button>
                </form>
            </td>

            <td>
                <!-- Excluir usuário -->
                <form action="/admin/user/delete" method="POST">
                    <input type="hidden" name="id" value="{{!u[0]}}">
                    <button type="submit" class="delete"
                        onclick="return confirm('Tem certeza que deseja apagar este usuário?')">
                        Excluir
                    </button>
                </form>
            </td>
        </tr>
        % end
    </table>

    <!-- Criar novo usuário -->
    <h3>➕ Criar Novo Usuário</h3>
    <form action="/admin/user/add" method="POST">
        <input type="text" name="username" placeholder="Novo usuário" required>
        <input type="password" name="password" placeholder="Senha" required>
        <button type="submit" class="add">Criar</button>
    </form>


    <!-- ============================ PLAYERS ============================ -->
    <h2>🎮 Jogadores (Players)</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Pontuação</th>
            <th>Ações</th>
        </tr>

        % for p in players:
        <tr>
            <td>{{p[0]}}</td>
            <td>{{p[1]}}</td>
            <td>{{p[2]}}</td>

            <td>
                <!-- Excluir player -->
                <form action="/players/delete" method="POST">
                    <input type="hidden" name="id" value="{{!p[0]}}">
                    <button type="submit" class="delete"
                        onclick="return confirm('Tem certeza que deseja apagar este player?')">
                        Excluir
                    </button>
                </form>
            </td>
        </tr>
        % end
    </table>

</body>
</html>
