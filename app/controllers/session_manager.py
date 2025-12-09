import uuid
from typing import Optional, List, Tuple
from app.models.database import Database
from datetime import datetime

db = Database()

class SessionManager:
    """
    Gerencia sessões de usuários com persistência no banco de dados.
    """

    @classmethod
    def create_session(cls, user_dict: dict) -> str:
        session_id = str(uuid.uuid4())
        user_id = user_dict["id"]
        created_at = datetime.now().isoformat()

        db.execute(
            "INSERT INTO sessions (session_id, user_id, created_at) VALUES (?, ?, ?)",
            (session_id, user_id, created_at)
        )
        return session_id

    @classmethod
    def get_session(cls, session_id: str) -> Optional[dict]:
        row = db.fetch_one("SELECT session_id, user_id FROM sessions WHERE session_id = ?", (session_id,))
        if row:
            user_id = row[1]
            user = db.fetch_one("SELECT id, username, is_admin FROM users WHERE id = ?", (user_id,))
            if user:
                return {"id": user[0], "username": user[1], "is_admin": bool(user[2])}
        return None

    @classmethod
    def delete_session(cls, session_id: str):
        db.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))

    @classmethod
    def is_admin(cls, session_id: str) -> bool:
        user = cls.get_session(session_id)
        return user.get("is_admin", False) if user else False

    @classmethod
    def list_sessions(cls) -> List[Tuple[str, str, bool]]:
        rows = db.fetch_all("SELECT session_id, user_id FROM sessions")
        sessions = []
        for session_id, user_id in rows:
            user = db.fetch_one("SELECT username, is_admin FROM users WHERE id = ?", (user_id,))
            if user:
                sessions.append((session_id, user[0], bool(user[1])))
        return sessions
