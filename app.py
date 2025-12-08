from flask import Flask, request, jsonify
from models import db, Todo
import os

app = Flask(__name__)

# === Configuración de la base de datos ===
# Render usa POSTGRES_URL
# Railway usa DATABASE_URL
uri = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")

# Corrige el formato postgres:// -> postgresql://
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# === RUTAS ===

@app.route("/")
def home():
    return jsonify({"status": "API RUNNING"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return jsonify([t.to_dict() for t in tasks])


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


@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    app.run()
