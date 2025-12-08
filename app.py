from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- Configuración de Flask y Base de Datos ---
app = Flask(__name__)
# Configura una base de datos SQLite en el archivo 'todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qnrHMSbEhHpzOWYHyWsEcgdOkckSkSyT@HOST:PORT/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- Rutas de la Aplicación ---

# Ruta para mostrar y agregar tareas
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Obtiene el contenido de la tarea del formulario
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            # Agrega la tarea a la base de datos y guarda
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Hubo un problema al añadir tu tarea.'
    else:
        # Muestra todas las tareas, ordenadas por fecha de creación
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Pasa las tareas al template HTML para que las muestre
        return render_template('index.html', tasks=tasks)

# Ruta para eliminar tareas
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Hubo un problema al eliminar esa tarea.'
        
# Ruta para marcar/desmarcar tareas (Toggle completion)
@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = Todo.query.get_or_404(id)
    # Cambia el estado: si es 0 (pendiente), lo pone a 1 (completado), y viceversa
    task_to_complete.completed = 1 if task_to_complete.completed == 0 else 0

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Hubo un problema al actualizar la tarea.'


if __name__ == '__main__':
    # Crea la base de datos si no existe
    with app.app_context():
        db.create_all()

    app.run(debug=True)
