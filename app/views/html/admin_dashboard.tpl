<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <style>
        body { font-family: Arial; background:#f3f3f3; padding:30px; }
        h1 { text-align:center; margin-bottom:40px; }
        h2 { margin-top:40px; }
        h3 { margin-top:20px; }
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
    <h2>🧑‍💻 Usuários</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Ações</th>
        </tr>

        % for u in usuarios:
        <tr>
            <td>{{u['id']}}</td>
            <td>
                <form action="/admin/user/update" method="POST">
                    <input type="hidden" name="id" value="{{u['id']}}">
                    <input type="text" name="username" value="{{u['username']}}" required>
                    <input type="password" name="password" placeholder="Nova senha (opcional)">
                    <button type="submit" class="update">Salvar</button>
                </form>
            </td>
            <td>
                <form action="/admin/user/delete" method="POST">
                    <input type="hidden" name="id" value="{{u['id']}}">
                    <button type="submit" class="delete"
                        onclick="return confirm('Tem certeza que deseja apagar este usuário?')">
                        Excluir
                    </button>
                </form>
            </td>
        </tr>
        % end
    </table>

    <h3>➕ Criar Novo Usuário</h3>
    <form action="/admin/user/add" method="POST">
        <input type="text" name="username" placeholder="Novo usuário" required>
        <input type="password" name="password" placeholder="Senha" required>
        <button type="submit" class="add">Criar</button>
    </form>

    <!-- ============================ PLAYERS ============================ -->
    <h2>🎮 Jogadores</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Pontuação</th>
            <th>Ações</th>
        </tr>

        % for p in players:
        <tr>
            <td>{{p.id}}</td>
            <td>{{p.user_id}}</td>
            <td>{{p.score}}</td>
            <td>
                <form action="/players/delete" method="POST">
                    <input type="hidden" name="id" value="{{p.id}}">
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
