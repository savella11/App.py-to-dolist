from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# ===============================
# CONFIGURACIÓN BD
# ===============================

url = os.getenv("DATABASE_URL")

# Algunos proveedores dan postgres:// → SQLAlchemy exige postgresql://
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===============================
# MODELO
# ===============================
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=0)


# ===============================
# RUTAS
# ===============================
@app.route("/")
def index():
    return {"status": "API RUNNING"}

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "content": t.content, "completed": t.completed}
        for t in tasks
    ])

@app.route("/tasks", methods=["POST"])
def add_task():
    try:
        data = request.get_json()
        
        # 1. Validación: Verificar que 'content' exista y no esté vacío
        content = data.get("content")
        
        # Si la clave 'content' no existe en el JSON o si su valor está vacío,
        # devolvemos un error 400 (Bad Request)
        if not content or content.strip() == "":
            return jsonify({"error": "Content field is required"}), 400
            
        # 2. Creación y Commit (esto ya no fallará por NOT NULL)
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task created", "id": new_task.id}), 201
        
    except Exception as e:
        # Esto captura errores de JSON malformado o de servidor
        print(f"Error during add_task: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id):
    t = Task.query.get_or_404(id)
    t.completed = not t.completed
    db.session.commit()
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    t = Task.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Task deleted"})


# ===============================
# RUN (solo local)
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


