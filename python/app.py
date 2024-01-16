#app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    db_path = os.path.join(app.root_path, 'todo.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Create a table called TODOS
def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS TODOS
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TASK TEXT NOT NULL,
                        STATUS TEXT NOT NULL,
                        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Function to add new ToDo
def add_todo(task):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TODOS (TASK, STATUS) VALUES (?, 'pending')", (task,))
    conn.commit()
    conn.close()


# Function to display ToDos by status
def view_todos_by_status(status):
    conn = get_db_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM TODOS WHERE STATUS = ?", (status,))
    else:
        cursor.execute("SELECT * FROM TODOS")
    todos = cursor.fetchall()
    conn.close()
    return todos

# Function to update the status of a ToDo
def update_status(id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE TODOS SET STATUS = ? WHERE ID = ?", (new_status, id))
    conn.commit()
    conn.close()

# Function to delete a ToDo
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

@app.route('/')
@app.route('/<status>')
def index(status=None):
    todos = view_todos_by_status(status)
    return render_template('index.html', todos=todos, status=status)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    add_todo(task)
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_status = request.form.get('status')
    update_status(id, new_status)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    delete_todo(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()  # Start the app and create the table if it doesn't exist
    app.run(host='0.0.0.0', debug=True)