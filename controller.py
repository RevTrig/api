from database import get_db


def insert_article(art_id, name, stock):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO articles (art_id, name, stock) VALUES (?, ?, ?) on conflict(art_id) do update set art_id=excluded.art_id, name=excluded.name, stock=excluded.stock;"
    cursor.execute(statement, [art_id, name, stock])
    db.commit()
    return True

def insert_products(name, price, contain_articles_id):
    db = get_db()
    db.row_factory = dict_factory
    cursor = db.cursor()
    check_statement = "SELECT count (*) as rows from products WHERE name=?"
    cursor.execute(check_statement, [name])
    rows = cursor.fetchone()
    
    if (rows['rows'] >0):
        return False
    else:
        statement = "INSERT INTO products (name, price, contain_articles_id) VALUES (?, ?, ?) "
        cursor.execute(statement, [name, price, contain_articles_id])
        db.commit()
        return True

def insert_contain_articles(contain_art_articles_id, article_art_id, amount_of):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO contain_article (contain_art_articles_id, article_art_id, amount_of) VALUES (?, ?, ?) "
    cursor.execute(statement, [contain_art_articles_id,article_art_id, amount_of])
    db.commit()
    return True

def delete_products(name):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM products WHERE name = ?"
    cursor.execute(statement, [name])
    db.commit()
    return True

def update_contain_articles(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM contain_article WHERE contain_art_articles_id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True


def get_contained_article_id(name):
    db= get_db()
    cursor = db.cursor()
    statement = "SELECT contain_articles_id FROM products WHERE name = ?"
    cursor.execute(statement, [name])
    result =cursor.fetchone()
    return result[0]


def get_articles_to_update(contain_art_articles_id):
    db = get_db()
    db.row_factory = dict_factory
    cursor = db.cursor()
    statement = "SELECT article_art_id , amount_of from contain_article where contain_art_articles_id= ? "
    cursor.execute(statement, [contain_art_articles_id])
    return cursor.fetchall()

def update_articles(id, sum):
    db =get_db()
    cursor = db.cursor()
    statement = "UPDATE articles SET stock = stock - ?  WHERE art_id = ?"
    cursor.execute(statement, [sum , id])
    db.commit()
    return True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        # col[0] is the column name
        d[col[0]] = row[idx]
    return d


def get_all_products():
    db = get_db()
    db.row_factory = dict_factory
    cursor = db.cursor()
    query = "SELECT  b.name as article, b.stock, a.amount_of,c.name,c.price  FROM contain_article a, articles b, products c WHERE a.article_art_id =b.art_id and a.contain_art_articles_id =c.contain_articles_id group by c.name ,b.art_id"
    cursor.execute(query) 
    return cursor.fetchall()

def load_products():
    db=get_db()
    db.row_factory = dict_factory
    cursor = db.cursor()
    query = "SELECT  name FROM products"
    cursor.execute(query)
    return cursor.fetchall()
