from flask import Flask, request, jsonify
from models import db, Todo
import os

app = Flask(__name__)

# === Configuración de la base de datos ===
uri = os.getenv("DATABASE_URL")

# Validación por si no está configurada en Render
if not uri:
    raise Exception("DATABASE_URL environment variable not set")

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# === Rutas de prueba ===
@app.route("/")
def home():
    return jsonify({"status": "API RUNNING"}), 200


# === GET: obtener todas las tareas ===
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return jsonify([t.to_dict() for t in tasks])


# === POST: crear tarea ===
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


# === PUT: marcar como completada ===
@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify(task.to_dict())


# === DELETE: eliminar tarea ===
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    app.run()

from flask_cors import CORS
CORS(app)

