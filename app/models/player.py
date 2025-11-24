import sqlite3

DB_NAME = 'bmvc.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

class Player:
    @staticmethod
    def all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, score FROM players')
        players = cursor.fetchall()
        conn.close()
        return [{'id': p[0], 'name': p[1], 'score': p[2]} for p in players]

    @staticmethod
    def create(name, score=0):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO players (name, score) VALUES (?, ?)', (name, score))
        conn.commit()
        conn.close()

    @staticmethod
    def update(player_id, name=None, score=None):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if name is not None:
            cursor.execute('UPDATE players SET name=? WHERE id=?', (name, player_id))
        if score is not None:
            cursor.execute('UPDATE players SET score=? WHERE id=?', (score, player_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(player_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM players WHERE id=?', (player_id,))
        conn.commit()
        conn.close()

init_db()
