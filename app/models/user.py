import sqlite3
import os
from app.config import DB_NAME
from bottle import request

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()


class User:

    @staticmethod
    def create(username, password):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()
        conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username = ? AND password = ?
        """, (username, password))

        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def all():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users ORDER BY id ASC")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def update(user_id, username, password=None):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if password:
            cursor.execute("""
                UPDATE users SET username=?, password=? WHERE id=?
            """, (username, password, user_id))
        else:
            cursor.execute("""
                UPDATE users SET username=? WHERE id=?
            """, (username, user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
    def usuario_admin():
        return request.get_cookie("is_admin") == "1"


