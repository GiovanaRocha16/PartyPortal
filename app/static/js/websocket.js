document.addEventListener("DOMContentLoaded", () => {
    const box = document.getElementById("ranking");

    // 1) Carrega ranking inicial
    function loadRanking(data) {
        box.innerHTML = "";
        data.forEach((p, i) => {
            box.innerHTML += `
                <div class="item">
                    <span>#${i+1}</span>
                    <span>${p.username}</span>
                    <span>${p.score}</span>
                </div>
            `;
        });
    }

    // 2) Fetch inicial (fallback)
    fetch("/api/ranking")
        .then(r => r.json())
        .then(loadRanking);

    // 3) WebSocket realtime
    const ws = new WebSocket("ws://" + window.location.host + "/ws/ranking");

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === "ranking_update") {
            loadRanking(data.ranking);
        }
    };


    ws.onerror = () => {
        console.log("WebSocket OFF, usando HTTP somente.");
    };
});
