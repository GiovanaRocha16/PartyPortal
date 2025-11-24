<h2>Gerenciar Jogadores</h2>

<form action="/players/add" method="post">
    <input type="text" name="name" placeholder="Nome do jogador" required>
    <button type="submit">Adicionar</button>
</form>

<table>
    <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Pontuação</th>
        <th>Ações</th>
    </tr>
    % for player in players:
    <tr>
        <td>{{player['id']}}</td>
        <td>{{player['name']}}</td>
        <td>{{player['score']}}</td>
        <td>
            <form action="/players/update" method="post" style="display:inline">
                <input type="hidden" name="id" value="{{player['id']}}">
                <input type="text" name="name" placeholder="Novo nome">
                <input type="number" name="score" placeholder="Nova pontuação">
                <button type="submit">Editar</button>
            </form>
            <form action="/players/delete" method="post" style="display:inline">
                <input type="hidden" name="id" value="{{player['id']}}">
                <button type="submit">Deletar</button>
            </form>
        </td>
    </tr>
    % end
</table>
