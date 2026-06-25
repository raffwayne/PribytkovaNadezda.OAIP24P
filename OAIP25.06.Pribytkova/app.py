from flask import Flask, request, jsonify
from db import init_db, get_db

app = Flask(__name__)
app.secret_key = 'secret_key_1234'


init_db()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    done = request.args.get('done')
    conn = get_db()
    
    if done is not None:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE done = ?", 
            (int(done),)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks").fetchall()
    
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", 
        (task_id,)
    ).fetchone()
    conn.close()
    
    if row is None:
        return jsonify({"error": "Не найдено"}), 404
    
    return jsonify(dict(row))


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    
    if not data or "title" not in data:
        return jsonify({"error": "Нужно поле title"}), 400
    
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (data["title"], int(data.get("done", 0)))
    )
    conn.commit()
    new_id = cur.lastrowid
    
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()
    conn.close()
    
    return jsonify(dict(row)), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    
    if row is None:
        conn.close()
        return jsonify({"error": "Не найдено"}), 404
    
    title = data.get("title", row["title"])
    done = int(data.get("done", row["done"]))
    
    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, done, task_id)
    )
    conn.commit()
    
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    conn.close()
    
    return jsonify(dict(row))


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    
    if row is None:
        conn.close()
        return jsonify({"error": "Не найдено"}), 404
    
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return "", 204

if __name__ == '__main__':
    app.run(debug=True)