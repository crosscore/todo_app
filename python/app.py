#app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(app.root_path, 'todo.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS TODOS
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TASK TEXT NOT NULL,
                        STATUS TEXT NOT NULL,
                        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ITEM_ORDER INTEGER)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def add_todo(task):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(ITEM_ORDER) FROM TODOS")
        max_order = cursor.fetchone()[0]
        next_order = 1 if max_order is None else max_order + 1
        cursor.execute("INSERT INTO TODOS (TASK, STATUS, ITEM_ORDER) VALUES (?, 'pending', ?)", (task, next_order))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def view_todos_by_status(status):
    conn = get_db_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM TODOS WHERE STATUS = ? ORDER BY ITEM_ORDER", (status,))
    else:
        cursor.execute("SELECT * FROM TODOS ORDER BY ITEM_ORDER")
    todos = cursor.fetchall()
    conn.close()
    return todos

def update_status(id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TODOS SET STATUS = ? WHERE ID = ?", (new_status, id))
    conn.commit()
    conn.close()

def delete_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TODOS WHERE ID = ?", (id,))
    conn.commit()
    conn.close()

@app.route('/todo/<int:id>')
def todo_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TODOS WHERE ID = ?", (id,))
    todo = cursor.fetchone()
    conn.close()
    return render_template('todo_detail.html', todo=todo)

@app.route('/reset')
def reset_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TODOS SET STATUS = 'pending'")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_task = request.form['task']
        cursor.execute("UPDATE TODOS SET TASK = ? WHERE ID = ?", (new_task, id))
        conn.commit()
        return redirect(url_for('todo_detail', id=id))

    cursor.execute("SELECT * FROM TODOS WHERE ID = ?", (id,))
    todo = cursor.fetchone()
    conn.close()
    return render_template('todo_detail.html', todo=todo)

@app.route('/')
@app.route('/<status>')
def index(status=None):
    todos = view_todos_by_status(status)
    return render_template('index.html', todos=todos, statusa=status)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    add_todo(task)
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_status = request.form['status']
    update_status(id, new_status)
    return '', 204

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_todo(id)
    return redirect(url_for('index'))

@app.route('/move/<int:id>/<direction>', methods=['POST'])
def move_item(id, direction):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ITEM_ORDER FROM TODOS WHERE ID = ?", (id,))
        current_order = cursor.fetchone()[0]
        if direction == 'up':
            cursor.execute("SELECT ID, ITEM_ORDER FROM TODOS WHERE ITEM_ORDER < ? ORDER BY ITEM_ORDER DESC LIMIT 1", (current_order,))
        elif direction == 'down':
            cursor.execute("SELECT ID, ITEM_ORDER FROM TODOS WHERE ITEM_ORDER > ? ORDER BY ITEM_ORDER ASC LIMIT 1", (current_order,))
        row = cursor.fetchone()
        if row:
            swap_id, swap_order = row
            cursor.execute("UPDATE TODOS SET ITEM_ORDER = -1 WHERE ID = ?", (id,))
            cursor.execute("UPDATE TODOS SET ITEM_ORDER = ? WHERE ID = ?", (current_order, swap_id))
            cursor.execute("UPDATE TODOS SET ITEM_ORDER = ? WHERE ID = ?", (swap_order, id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return '', 500 # Internal Server Error
    finally:
        conn.close()
        return '', 204 # No Content


if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', debug=True)