import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SAVE_DIR = BASE_DIR / "backend"
DEFAULT_DB_PATH = SAVE_DIR / "back.db"

def connect_db():
    return sqlite3.connect(DEFAULT_DB_PATH)

def get_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parameter, unit FROM categories")
    categories = []
    for row in cursor.fetchall():
        categories.append({
            'id': row[0],
            'name': row[1],
            'parameter': row[2],
            'unit': row[3]
        })
    conn.close()
    return categories


# bdinit.py

def get_items(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Добавляем category_id в запрос (второй столбец)
    cursor.execute("""
        SELECT 
            id, 
            name, 
            category_id,
            parameter_value, 
            unit, 
            cost_price, 
            selling_price, 
            image_id 
        FROM items 
        WHERE category_id = ?
    """, (category_id,))

    items = []
    for row in cursor.fetchall():
        items.append({
            'id': row[0],  # id
            'name': row[1],  # name
            'category_id': row[2],
            'parameter_value': row[3],
            'unit': row[4],
            'cost_price': row[5],
            'selling_price': row[6],
            'image_id': row[7]
        })
    conn.close()
    return items