import sqlite3


def create_table():
    connection = sqlite3.connect('full_info.db')
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS info
                 (image TEXT, title TEXT, calories TEXT, carbs TEXT, fat TEXT, protein TEXT, link TEXT)''')
    connection.commit()
    connection.close()


def insert_data(image, title, calories, carbs, fat, protein, link):
    connection = sqlite3.connect('full_info.db')
    c = connection.cursor()
    c.execute('SELECT * FROM info WHERE title=?', (title,))
    row = c.fetchone()
    if row is None:
        c.execute("INSERT INTO info (image, title, calories, carbs, fat, protein, link) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (image, title, calories, carbs, fat, protein, link))
        print("Новый данные добавлены")
    connection.commit()
    connection.close()


def get_info_by_title(info, title):
    connection = sqlite3.connect('full_info.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT {info} FROM info WHERE title = '{title}'")
    data = cursor.fetchall()
    connection.close()
    if info == "link":
        return f"https://www.eatthismuch.com/{data[0][0]}"
    else:
        return data[0][0]
