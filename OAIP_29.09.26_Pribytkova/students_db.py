import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    grade INTEGER NOT NULL,
    age INTEGER)""")
    conn.commit()

def add_initial_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        students = [
            ("Иванов Иван", "ИСП-101", 5, 16),
            ("Петров Петр", "ИСП-101", 4, 17),
            ("Сидоров Алексей", "ИСП-102", 3, 18),
            ("Смирнова Анна", "ИСП-102", 5, 19),
            ("Кузнецов Максим", "ИСП-101", 4, 18),]
        cursor.executemany("INSERT INTO students(name, group_name, grade, age) VALUES (?, ?, ?, ?)", students)
        conn.commit()
        print ("Добавлено 5 студенттов")

def show_all_students (conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, group_name, grade, age FROM students")
    rows = cursor.fetchall()
    if not rows:
        print("Студентов нет в базе")
        return
    print (f"{'ID':<4} {'ФИО':<22} {'Группа':<10} {'Оценка':<7} {'Возраст':<7}")
    print("-" * 55)
    for r in rows:
        print(f"{r[0]:<4} {r[1]:<22} {r[2]:<10} {r[3]:<7} {r[4] if r[4] is not None else '-':<7}")
    print()

def add_student(conn):
    name = input("Введите ФИО студента: ").strip()
    group_name = input("Введите группу: ").strip()
    try:
        grade = int(input("Введите оценку: "))
        age = int(input("Введите возраст: "))
    except ValueError:
        print("Ошибка: оценка и возраст ддолжны быть числами")
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)",
        (name, group_name, grade, age))
    conn.commit()
    print("Студент добавлен")

def search_by_group(conn):
    group_name = input("Введите названиие группы: ").strip()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students WHERE group_name = ?", (group_name,))
    rows = cursor.fetchall()
    if not rows:
        print ("Студентов нет в группе")
        return
    print (f"Студенты группы {group_name}:")
    for r in rows:
        print(f"ID: {r[0]} | {r[1]} | Оценка: {r[3]} | Возраст: {r[4]}")
    print()

def search_by_grade(conn):
    try:
        grade = int(input("Введите оценку: ").strip())
    except ValueError:
        print ("Ошибка: оценка должна быть числом")
        return
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students WHERE grade = ?", (grade,))
    rows = cursor.fetchall()
    if not rows:
        print (f"Студентов с оценкой {grade} нет")
        return
    print (f"Студенты с оценкой {grade}:")
    for r in rows:
        print(f"ID: {r[0]} | {r[1]} | Возраст: {r[4]}")
    print()

def change_grade(conn):
    try:
        sid = int(input("Введите ID студента: "))
        new_grade = int(input("Введите новую оценку: "))
    except ValueError:
        print("Ошибка: ID и оценка должны быть числом")
        return
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET grade = ? WHERE id = ?", (new_grade, sid))
    conn.commit()
    if cursor.rowcount == 0:
        print(f"Студент с ID {sid} не найден")
    else: 
        print("Оценка изменена")

def delete_student(conn):
    try:
        sid = int(input("Введите  ID студента для удаления: "))
    except ValueError:
        print("Ошибка: ID студента должен быть числом")
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (sid,))
    conn.commit()
    if cursor.rowcount == 0:
        print(f"Студент с ID {sid} не найден")
    else:
        print("Студент удален. Оставшиеся студенты:")
        show_all_students(conn)

def show_average_grade(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM students")
    avg = cursor.fetchone()[0]
    if avg is None:
        print("В базе нет студентов")
    else:
        print(f"Средняя оценка студентов: {avg:.2f}")

def menu(conn):
    while True:
        print("====УЧЕТ СТУДЕНТОВ====")
        print("1. Показать всех студентов")
        print("2. Добавить студента")
        print("3. Найти студентов по группе")
        print("4. Найти студентов по оценке")
        print("5. Изменить оценку")
        print("6. Удалить студента")
        print("7. Средняя оценка всех студентов")
        print("0. Выход")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            show_all_students(conn)
        elif choice == "2":
            add_student(conn)
        elif choice == "3":
            search_by_group(conn)
        elif choice == "4":
            search_by_grade(conn)
        elif choice == "5":
            change_grade(conn)
        elif choice == "6":
            delete_student(conn)
        elif choice == "7":
            show_average_grade(conn)
        elif choice == "0":
            print ("Выход из программы")
            break
        else:
            print("Неверный пункт меню")

def main():
    conn = get_connection()
    try:
        init_db(conn)
        add_initial_students(conn)
        menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()


