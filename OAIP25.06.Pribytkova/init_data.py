from db import init_db, get_db

# Создаем таблицу
init_db()

# Добавляем тестовые задачи
conn = get_db()
conn.execute(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    ("Купить молоко", 0)
)
conn.execute(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    ("Сделать домашку", 1)
)
conn.execute(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    ("Погулять с собакой", 0)
)
conn.commit()
conn.close()

