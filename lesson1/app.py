from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

STUDENTS = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return {"you sent": data}


@app.get("/")
def index():
    return {"message": "Hello, API!"}


@app.post("/students")
def create_student():
    body = request.get_json(silent=True) or {}
    name = body.get("name")

    if not name:
        return {"error": "name is required"}, 400

    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0),
    }

    STUDENTS.append(student)

    return student, 201
