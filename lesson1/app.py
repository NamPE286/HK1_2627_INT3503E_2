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


BOOKS = [{"id": 1, "title": "Clean Code", "author": "R. Martin"}]
_next = 2


def find_book(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)


@app.get("/books")
def list_books():
    try:
        limit = int(request.args.get("limit", 100))
    except ValueError:
        return {"error": "limit must be a non-negative integer"}, 400

    if limit < 0:
        return {"error": "limit must be a non-negative integer"}, 400

    return BOOKS[:limit]


@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = find_book(book_id)

    if book is None:
        return {"error": "not found"}, 404

    return book


@app.post("/books")
def create_book():
    global _next
    body = request.get_json(silent=True)
    t, a = body.get("title"), body.get("author")

    if not t or not a:
        return {"error": "need title+author"}, 400

    book = {"id": _next, "title": body["title"], "author": body["author"]}
    _next += 1
    BOOKS.append(book)

    return book, 201, {"Location": f"/books/{book['id']}"}

@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find_book(bid)
    
    if not book:
        return {"error": "not found"}, 404
    
    if request.method == "PUT":
        book.update(request.get_json(silent=True) or {})
        return book, 200
    
    BOOKS.remove(book)
    
    return "", 204


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
