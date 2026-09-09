from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)


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


STUDENTS = []


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


def find_by_id(id):
    if id == "123":
        return {"id": id, "name": "abc"}

    return None


@app.get("/books/<book_id>")
def get_book(book_id):
    book = find_by_id(book_id)

    if book is None:
        return {"error": "not found"}, 404

    return book


@app.get("/items/<int:item_id>")
def get_item(item_id):
    return {"id": item_id}


ORDERS = {}


@app.delete("/orders/<order_id>")
def delete_order(order_id):
    order = ORDERS.get(order_id)

    if order is None:
        return {"error": "not found"}, 404

    if order["status"] in ("shipped", "delivered"):
        return {"error": "cannot delete"}, 409

    ORDERS.pop(order_id, None)
    
    return "", 204
