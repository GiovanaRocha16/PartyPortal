<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🎰 Caça-Níquel</title>

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);
            text-align: center;
            padding: 40px;
            color: white;
        }

        h1 {
            font-size: 34px;
            margin-bottom: 20px;
        }

        .slot-machine {
            display: flex;
            justify-content: center;
            margin: 30px auto;
            gap: 20px;
        }

        .slot {
            width: 80px;
            height: 80px;
            background: white;
            color: black;
            font-size: 40px;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.35);
        }

        button {
            background-color: #6a1b9a;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 20px;
            box-shadow: 0 4px #4a0d6e;
        }

        button:active {
            box-shadow: none;
            transform: translateY(3px);
        }

        /* botão de voltar */
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

    <h1>🎰 Caça-Níquel Animado</h1>

    <div class="slot-machine">
        <div class="slot" id="s1">🍒</div>
        <div class="slot" id="s2">🍋</div>
        <div class="slot" id="s3">⭐</div>
    </div>

    <button onclick="girar()">🎲 Girar</button>

    <h2 id="resultado"></h2>

    <!-- botão voltar -->
    <a href="/" class="btn-voltar">⬅️ Voltar ao Menu</a>

    <script>
        const simbolos = ["🍒", "🍋", "🍉", "⭐", "🔔", "🍇"];

        function girar() {
            let s1 = document.getElementById("s1");
            let s2 = document.getElementById("s2");
            let s3 = document.getElementById("s3");
            let texto = document.getElementById("resultado");

            texto.innerHTML = "";

            // animação girando
            let intervalo = setInterval(() => {
                s1.innerHTML = simbolos[Math.floor(Math.random() * simbolos.length)];
                s2.innerHTML = simbolos[Math.floor(Math.random() * simbolos.length)];
                s3.innerHTML = simbolos[Math.floor(Math.random() * simbolos.length)];
            }, 80);

            // parar depois de 1.5s
            setTimeout(() => {
                clearInterval(intervalo);

                let final1 = simbolos[Math.floor(Math.random() * simbolos.length)];
                let final2 = simbolos[Math.floor(Math.random() * simbolos.length)];
                let final3 = simbolos[Math.floor(Math.random() * simbolos.length)];

                s1.innerHTML = final1;
                s2.innerHTML = final2;
                s3.innerHTML = final3;

                if (final1 === final2 && final2 === final3) {
                    texto.innerHTML = "🎉 Parabéns, você ganhou!!! Três iguais!!!";
                } else {
                    texto.innerHTML = "Tente novamente!";
                }
            }, 1500);
        }
    </script>

</body>
</html>
