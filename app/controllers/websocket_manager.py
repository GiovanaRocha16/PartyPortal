
from geventwebsocket.websocket import WebSocket
import json

class WebSocketManager:
    """
    Gerencia conexões WebSocket e permite broadcast
    seguindo boas práticas de separação de responsabilidades.
    """

    def __init__(self):
        self.connections = set()

    # ---------------------------
    # CONEXÕES
    # ---------------------------
    def add_connection(self, ws: WebSocket):
        """Adiciona um cliente conectado."""
        if ws and not ws.closed:
            self.connections.add(ws)

    def remove_connection(self, ws: WebSocket):
        """Remove uma conexão encerrada."""
        if ws in self.connections:
            self.connections.remove(ws)

    # ---------------------------
    # ENVIO
    # ---------------------------
    def send(self, ws: WebSocket, data: dict):
        """Envia mensagem individual."""
        if ws and not ws.closed:
            ws.send(json.dumps(data))

    def broadcast(self, data: dict):
        """Envia mensagem para todos os clientes conectados."""
        dead = []
        for ws in self.connections:
            try:
                if ws.closed:
                    dead.append(ws)
                else:
                    ws.send(json.dumps(data))
            except:
                dead.append(ws)

        for ws in dead:
            self.remove_connection(ws)
    
    def broadcast_ranking(self, player_ctrl, user_ctrl):
        """Envia o ranking atualizado para todos os clientes conectados."""
        ranking = player_ctrl.get_ranking(user_ctrl)
        data = {"event": "ranking_update", "ranking": ranking}
        self.broadcast(data)

        
    # ---------------------------
    # HANDLER PRINCIPAL
    # ---------------------------
    def handle_connection(self, ws):
        """Loop principal do WebSocket."""
        self.add_connection(ws)

        try:
            while not ws.closed:
                msg = ws.receive()
                if msg is None:
                    break
                self.send(ws, {"event": "echo", "message": msg})
        finally:
            self.remove_connection(ws)

# Cria uma instância global que pode ser importada
ws_manager = WebSocketManager()

