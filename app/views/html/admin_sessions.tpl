<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Admin Sessions</title>
    <style>
        body { font-family: Arial; background:#f3f3f3; padding:30px; }
        h1 { text-align:center; margin-bottom:40px; }
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
            background:#b30000;
            color:white;
            border:none;
            border-radius:4px;
        }
    </style>
</head>
<body>

    <h1>🔒 Sessões Ativas</h1>

    <table>
        <tr>
            <th>Session ID</th>
            <th>Username</th>
            <th>Admin?</th>
            <th>Ações</th>
        </tr>

        % for s in sessions:
        <tr>
            <td>{{s[0]}}</td>
            <td>{{s[1]}}</td>
            <td>{{'Sim' if s[2] else 'Não'}}</td>
            <td>
                <form action="/admin/session/delete" method="POST">
                    <input type="hidden" name="session_id" value="{{!s[0]}}">
                    <button type="submit"
                        onclick="return confirm('Tem certeza que deseja apagar esta sessão?')">
                        Excluir
                    </button>
                </form>
            </td>
        </tr>
        % end
    </table>

</body>
</html>
