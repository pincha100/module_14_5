import sqlite3


def initiate_db():
    """Создаёт таблицы Products и Users, если они ещё не созданы."""
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    # Создание таблицы Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    """)

    # Создание таблицы Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def add_products():
    """Добавляет тестовые данные в таблицу Products."""
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO Products (title, description, price)
        VALUES (?, ?, ?)
    """, [
        ("Product1", "Описание для Product1", 100),
        ("Product2", "Описание для Product2", 200),
        ("Product3", "Описание для Product3", 300),
        ("Product4", "Описание для Product4", 400)
    ])
    connection.commit()
    connection.close()


def get_all_products():
    """Возвращает все записи из таблицы Products."""
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products


def add_user(username, email, age):
    """Добавляет нового пользователя в таблицу Users."""
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
    """, (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    """Проверяет, есть ли пользователь с указанным именем в таблице Users."""
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user is not None
