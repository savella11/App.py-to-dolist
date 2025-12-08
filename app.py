from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Ruta de prueba
@app.route("/")
def index():
    return {"status": "API RUNNING"}

# Obtener tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "content": t.content, "completed": t.completed}
        for t in tasks
    ])

# Crear tarea
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = Task(content=data["content"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201

# Completar tarea
@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id):
    t = Task.query.get_or_404(id)
    t.completed = True
    db.session.commit()
    return jsonify({"message": "Task completed"})

# Eliminar tarea
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    t = Task.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

# Ejecutar en Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

