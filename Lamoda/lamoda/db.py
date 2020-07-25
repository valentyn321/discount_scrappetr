import sqlite3


def init_db(name_of_table: str, force: bool = False):
    conn = sqlite3.connect(name_of_table)
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS sales')

    c.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id              INTEGER PRIMARY KEY,
                brand           TEXT NOT NULL,
                title           TEXT NOT NULL,
                link            TEXT NOT NULL,
                price           REAL NOT NULL,
                sizes           TEXT NOT NULL,
                sex             TEXT NOT NULL
            )
    """)

    conn.commit()

def add_item(brand: str, title: str, link: str, price: float,  sizes: str, sex: str, name_of_table):
    conn = sqlite3.connect(name_of_table)
    c = conn.cursor()
    c.execute(
        'INSERT INTO sales (brand, title, link, price, sizes, sex) VALUES (?, ?, ?, ?, ?, ?)',
        (brand, title, link, price, sizes, sex)
    )
    conn.commit()
init_db('lamoda_shoes.db', force=True)