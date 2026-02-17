import json
import os

DATA_FILE = 'data.json'

STATUS_PLANNING = "Планирование"
STATUS_IN_PROGRESS = "В работе"
STATUS_DONE = "Готов"
VALID_STATUSES = [STATUS_PLANNING, STATUS_IN_PROGRESS, STATUS_DONE]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"projects": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"projects": []}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False

def get_next_project_id(projects):
    if not projects:
        return 1
    return max(p['id'] for p in projects) + 1

def get_next_task_id(tasks):
    if not tasks:
        return 1
    return max(t['id'] for t in tasks) + 1

def show_projects(data):
    projects = data.get('projects', [])
    if not projects:
        print("\nСписок проектов пуст")
        return
    print("\n=== СПИСОК ПРОЕКТОВ ===")
    print(f"{'ID':<5} {'Название':<20} {'Статус':<15} {'Задач':<10}")
    print("-" * 55)
    for proj in projects:
        task_count = len(proj.get('tasks', []))
        print(f"{proj['id']:<5} {proj['name']:<20} {proj['status']:<15} {task_count:<10}")
    print("-" * 55)

def create_project(data):
    name = input("\nВведите название нового проекта: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return
    print("Выберите начальный статус:")
    for i, status in enumerate(VALID_STATUSES, 1):
        print(f"{i}. {status}")
    try:
        choice = int(input("Ввод (цифра): "))
        if 1 <= choice <= len(VALID_STATUSES):
            status = VALID_STATUSES[choice - 1]
        else:
            status = STATUS_PLANNING
    except ValueError:
        status = STATUS_PLANNING

    new_id = get_next_project_id(data['projects'])
    new_project = {
        "id": new_id,
        "name": name,
        "status": status,
        "tasks": []
    }
    data['projects'].append(new_project)
    if save_data(data):
        print(f"Проект '{name}' создан с ID: {new_id}")
    else:
        print("Не удалось сохранить проект.")

def add_task(data):
    show_projects(data)
    if not data['projects']:
        return
    try:
        proj_id = int(input("\nВведите ID проекта: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    project = next((p for p in data['projects'] if p['id'] == proj_id), None)
    if not project:
        print("Проект не найден.")
        return
    task_name = input("Введите название задачи: ").strip()
    if not task_name:
        print("Название задачи не может быть пустым.")
        return
    new_task_id = get_next_task_id(project['tasks'])
    new_task = {
        "id": new_task_id,
        "title": task_name,
        "done": False
    }
    project['tasks'].append(new_task)
    if save_data(data):
        print(f"Задача '{task_name}' добавлена в проект '{project['name']}'")
    else:
        print("Не удалось сохранить задачу.")

def show_project_tasks(data):
    show_projects(data)
    if not data['projects']:
        return
    try:
        proj_id = int(input("\nВведите ID проекта для просмотра задач: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    project = next((p for p in data['projects'] if p['id'] == proj_id), None)
    if not project:
        print("Проект не найден.")
        return
    print(f"\n=== ЗАДАЧИ ПРОЕКТА: {project['name']} ===")
    tasks = project.get('tasks', [])
    if not tasks:
        print("В этом проекте нет задач.")
        return
    print(f"{'ID':<5} {'Название':<30} {'Статус'}")
    print("-" * 45)
    for task in tasks:
        status_str = "[x] Выполнено" if task['done'] else "[ ] Не выполнено"
        print(f"{task['id']:<5} {task['title']:<30} {status_str}")
    print("-" * 45)

def change_project_status(data):
    show_projects(data)
    if not data['projects']:
        return
    try:
        proj_id = int(input("\nВведите ID проекта для изменения статуса: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    project = next((p for p in data['projects'] if p['id'] == proj_id), None)
    if not project:
        print("Проект не найден.")
        return
    print(f"\nТекущий статус: {project['status']}")
    print("Доступные статусы:")
    for i, status in enumerate(VALID_STATUSES, 1):
        print(f"{i}. {status}")
    try:
        choice = int(input("Выберите новый статус (цифра): "))
        if 1 <= choice <= len(VALID_STATUSES):
            project['status'] = VALID_STATUSES[choice - 1]
            if save_data(data):
                print(f"Статус изменен на: {project['status']}")
            else:
                print("Ошибка сохранения.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Некорректное значение.")

def main():
    while True:
        print("\n=== МЕНЕДЖЕР ПРОЕКТОВ ===")
        print("1. Показать проекты")
        print("2. Создать проект")
        print("3. Добавить задачу")
        print("4. Показать задачи в проекте")
        print("5. Изменить статус проекта")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")
        data = load_data()

        if choice == '1':
            show_projects(data)
        elif choice == '2':
            create_project(data)
        elif choice == '3':
            add_task(data)
        elif choice == '4':
            show_project_tasks(data)
        elif choice == '5':
            change_project_status(data)
        elif choice == '0':
            print("Выход.")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()