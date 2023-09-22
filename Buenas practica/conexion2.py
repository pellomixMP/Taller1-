from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos Access
connection = pyodbc.connect(
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\cuc\Documents\Buenas practica\TasksDB.accdb;'
)

cursor = connection.cursor()

# Ruta principal para mostrar tareas


@app.route('/')
def index():
    cursor.execute('SELECT * FROM tasksDB')
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# Ruta para agregar una nueva tarea


@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    cursor.execute(
        'INSERT INTO tasksDB (Descripcion, Estado) VALUES (?, ?)', (task_name, False))
    connection.commit()
    return redirect(url_for('index'))

# Ruta para marcar una tarea como hecha o no hecha


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    cursor.execute('SELECT Estado FROM tasksDB WHERE Id = ?', (task_id,))
    task = cursor.fetchone()
    if task:
        new_done = not task[0]
        cursor.execute(
            'UPDATE tasksDB SET Estado = ? WHERE Id = ?', (new_done, task_id))
        connection.commit()
    return redirect(url_for('index'))

# Ruta para eliminar una tarea


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cursor.execute('DELETE FROM tasksDB WHERE id = ?', (task_id,))
    connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
