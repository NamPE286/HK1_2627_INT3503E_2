from flask import Flask, make_response, request

app = Flask(__name__)
books = []
next_id = 1


def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)


def get_pagination():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 20))
    except ValueError:
        return None

    return max(page, 1), max(1, min(size, 100))


def filter_books():
    data = books
    author = request.args.get("author")
    query = request.args.get("q", "").lower()

    if author:
        data = [book for book in data if book["author"].lower() == author.lower()]

    if query:
        data = [book for book in data if query in book["title"].lower()]

    return data


def pagination_links(page, size, total):
    last = max((total + size - 1) // size, 1)

    def url(target):
        return f"/books?page={target}&size={size}"

    links = {
        "self": {"href": url(page)},
        "first": {"href": url(1)},
        "last": {"href": url(last)},
    }

    if page > 1:
        links["prev"] = {"href": url(page - 1)}

    if page < last:
        links["next"] = {"href": url(page + 1)}

    return links, last


@app.get("/books")
def list_books():
    pagination = get_pagination()

    if pagination is None:
        return {"error": "page and size must be int"}, 400

    page, size = pagination
    data = filter_books()
    total = len(data)
    start = (page - 1) * size
    links, last = pagination_links(page, size, total)

    body = {
        "data": data[start:start + size],
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": last if total else 0,
        },
        "_links": links,
    }

    response = make_response(body)
    response.headers["Cache-Control"] = "public, max-age=30"
    return response


@app.post("/books")
def create_book():
    global next_id

    data = request.get_json()
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()

    if not title or not author:
        return {"error": "title and author required"}, 422

    book = {"id": next_id, "title": title, "author": author}
    books.append(book)
    next_id += 1

    response = make_response(book, 201)
    response.headers["Location"] = f"/books/{book['id']}"
    return response


@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = find_book(book_id)

    if book is None:
        return {"error": "not found"}, 404

    response = make_response(book)
    response.headers["Cache-Control"] = "max-age=60"
    return response


@app.put("/books/<int:book_id>")
def replace_book(book_id):
    book = find_book(book_id)

    if book is None:
        return {"error": "not found"}, 404

    data = request.get_json()
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()

    if not title or not author:
        return {"error": "need title+author"}, 422

    book.clear()
    book.update(
        id=book_id,
        title=title,
        author=author,
        isbn=data.get("isbn"),
        price=data.get("price"),
    )
    return book


@app.patch("/books/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)

    if book is None:
        return {"error": "not found"}, 404

    data = request.get_json()

    if data.get("price", 0) < 0:
        return {"error": "price must be positive"}, 422

    for field in ("title", "author", "isbn", "price"):
        if field in data:
            book[field] = data[field]

    return book


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return {"error": "not found"}, 404

    books.remove(book)
    return "", 204
