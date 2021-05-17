import sqlite3
DATABASE_NAME = "data.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS articles (art_id INTEGER PRIMARY KEY, name TEXT, stock INTEGER)
            """,
        """CREATE TABLE IF NOT EXISTS products ( name TEXT PRIMARY KEY, price FLOAT, contain_articles_id TEXT ,FOREIGN KEY(contain_articles_id) REFERENCES contain_article(contain_art_articles_id))""",
        """CREATE TABLE IF NOT EXISTS contain_article (contain_art_articles_id TEXT, article_art_id INTEGER, amount_of INTEGER, FOREIGN KEY(article_art_id) REFERENCES articles(art_id))"""
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)