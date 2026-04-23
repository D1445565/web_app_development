import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳與 SQLite 的連線，並開啟外鍵支援"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用 dict 的方式存取欄位
    conn.execute('PRAGMA foreign_keys = ON')  # 啟用外鍵約束，確保級聯刪除有效
    return conn

def init_db():
    """根據 schema.sql 初始化資料庫"""
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
