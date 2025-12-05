import sqlite3
import os
from app.config import DB_NAME

print(">>> BANCO SENDO USADO EM:", DB_NAME)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NULL,
            name TEXT,
            score INTEGER DEFAULT 0,
            history TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

class Player:
    @staticmethod
    def create(name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO players (user_id, name, score, history)
            VALUES (?, ?, ?, ?)
        """, (None, name, 0, f"Player {name} criado"))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id, name, score):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE players
            SET name=?, score=?, history=?
            WHERE id=?
        """, (name, score, f"Nome alterado para {name}", id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players WHERE id=?", (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def create_for_user(user_id, username):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO players (user_id, name, score)
                VALUES (?, ?, 0)
            """, (user_id, username))
            conn.commit()
        finally:
            if conn:
                conn.close()


    @staticmethod
    def get_by_user(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, score, history FROM players WHERE user_id=?", (user_id,))
        p = cursor.fetchone()
        conn.close()
        return p

    @staticmethod
    def add_score(user_id, amount):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET score = score + ? WHERE user_id=?", (amount, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT players.id,
                COALESCE(users.username, players.name),
                players.score
            FROM players
            LEFT JOIN users ON users.id = players.user_id
            ORDER BY players.score DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [{'id': r[0], 'username': r[1], 'score': r[2]} for r in rows]

init_db()
