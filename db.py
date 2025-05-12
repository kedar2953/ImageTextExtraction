import sqlite3

def create_db():
    conn = sqlite3.connect('image_data.db')
    c = conn.cursor()

    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS image_text_index
        USING fts5(image_name, extracted_text);
    ''')

    conn.commit()
    conn.close()

create_db()
