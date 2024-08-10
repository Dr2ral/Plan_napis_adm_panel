import sqlite3

def get_all_products():
    conn = sqlite3.connect("not_telegram.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL);
    ''')
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price) VALUES(?,?,?)', (f'Продукт{i}', f'{i}', i*100))
    res = conn.cursor().execute("SELECT * FROM Products").fetchall()
    conn.commit()
    conn.close()
    return res