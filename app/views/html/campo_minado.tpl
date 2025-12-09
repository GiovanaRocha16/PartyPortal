<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>💣 Campo Minado</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body style="text-align:center; font-family:sans-serif;">

    <h1>💣 Campo Minado</h1>
    <p>Clique nos campos para tentar não pisar na bomba!</p>

    % if resultado:
        <h2>{{resultado}}</h2>
    % end

    % if not acabou:
        <form method="post">

            % for i in range(1, 10):
                % if i in clicados:
                    <button disabled style="width:60px;height:60px;background:#ccc;">{{i}}</button>
                % else:
                    <button name="escolha" value="{{i}}" style="width:60px;height:60px;">{{i}}</button>
                % end

                % if i % 3 == 0:
                    <br>
                % end
            % end

            <input type="hidden" name="clicados" value="{{','.join(map(str, clicados))}}">
            <input type="hidden" name="bomba" value="{{bomba}}">
        </form>
    % end

    % if acabou:
        <a href="/campo_minado"
           style="display:inline-block;
                  background-color:#1976d2;
                  color:white;
                  padding:12px 24px;
                  border-radius:12px;
                  text-decoration:none;
                  font-weight:bold;
                  box-shadow:0 4px #4a116e;
                  margin-top:20px;">
            🔄 Tentar novamente
        </a>
    % end

    <br><br>

    <a href="/" 
       style="display:inline-block;
              background-color:#6a1b9a;
              color:white;
              padding:12px 24px;
              border-radius:12px;
              text-decoration:none;
              font-weight:bold;
              box-shadow:0 4px #4a116e;">
       ⬅️ Voltar ao Menu
    </a>

</body>
</html>
