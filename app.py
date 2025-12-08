from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Todo
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Obtener todas las tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return jsonify([t.to_dict() for t in tasks])

# Crear nueva tarea
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "content required"}), 400

    task = Todo(content=content)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Completar tarea
@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify(task.to_dict())

# Eliminar tarea
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200

@app.route("/")
def home():
    return jsonify({"status": "API RUNNING"}), 200

if __name__ == "__main__":
    app.run()
