import sqlite3
import os
from datetime import datetime

DB_PATH = "app/models/app.db"

class Database:
    def __init__(self, path=DB_PATH):
        self.path = path
        self.initialize_database()

    def connect(self):
        return sqlite3.connect(self.path)

    def initialize_database(self):
        con = self.connect()
        cur = con.cursor()

        # TABELA USERS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        );
        """)

        # TABELA PLAYERS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)

        # TABELA SESSIONS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)

        con.commit()
        con.close()

    # -------------------------
    # EXECUTE / INSERT / UPDATE / DELETE
    # -------------------------
    def execute(self, query, params=()):
        con = self.connect()
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        con.close()
        return True

    # -------------------------
    # SELECT individual
    # -------------------------
    def fetch_one(self, query, params=()):
        con = self.connect()
        cur = con.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
        con.close()
        return row

    # -------------------------
    # SELECT glbal
    # -------------------------
    def fetch_all(self, query, params=()):
        con = self.connect()
        cur = con.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        con.close()
        return rows

    # -------------------------
    # RETORNA O ÚLTIMO ID INSERIDO
    # -------------------------
    def last_insert_id(self, query, params=()):
        con = self.connect()
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        last_id = cur.lastrowid
        con.close()
        return last_id

