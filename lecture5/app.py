from flask import Flask, request, jsonify
from models import db, Book, Author, Category
from pagination import list_books, DEFAULT_LIMIT

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def seed():
    # chi seed 1 lan
    if Category.query.first() is not None:
        return

    tech = Category(name="Technology", slug="tech")
    fiction = Category(name="Fiction", slug="fiction")
    db.session.add(tech)
    db.session.add(fiction)
    db.session.flush()

    bob = Author(name="Robert C. Martin", bio="Uncle Bob")
    fowler = Author(name="Martin Fowler", bio="")
    rowling = Author(name="J.K. Rowling", bio="Harry Potter")
    db.session.add(bob)
    db.session.add(fowler)
    db.session.add(rowling)
    db.session.flush()

    # data mau
    b1 = Book(title="Clean Code", isbn="9780132350884", price_vnd=450000,
              stock=12, genre="tech", category_id=tech.id)
    b1.authors = [bob]

    b2 = Book(title="Refactoring", isbn="9780134757599", price_vnd=520000,
              stock=8, genre="tech", category_id=tech.id)
    b2.authors = [fowler]

    b3 = Book(title="Harry Potter 1", isbn="9780747532699", price_vnd=180000,
              stock=30, genre="fiction", category_id=fiction.id)
    b3.authors = [rowling]

    b4 = Book(title="Harry Potter 2", isbn="9780747538493", price_vnd=190000,
              stock=25, genre="fiction", category_id=fiction.id)
    b4.authors = [rowling]

    b5 = Book(title="Clean Architecture", isbn="9780134494166", price_vnd=480000,
              stock=10, genre="tech", category_id=tech.id)
    b5.authors = [bob]

    b6 = Book(title="The Pragmatic Programmer", isbn="9780135957059",
              price_vnd=410000, stock=15, genre="tech", category_id=tech.id)
    b6.authors = [bob, fowler]

    b7 = Book(title="Design Patterns", isbn="9780201633610", price_vnd=420000,
              stock=9, genre="tech", category_id=tech.id)
    b7.authors = [fowler]

    b8 = Book(title="Dune", isbn="9780441172719", price_vnd=230000,
              stock=11, genre="fiction", category_id=fiction.id)

    db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8])
    db.session.commit()


_ready = False


@app.before_request
def setup():
    global _ready
    if not _ready:
        db.create_all()
        seed()
        _ready = True


@app.get("/api/v1/books")
def get_books():
    strategy = request.args.get("strategy", "cursor")
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", DEFAULT_LIMIT, type=int)
    cursor = request.args.get("cursor")
    sort = request.args.get("sort", "-id")
    genre = request.args.get("genre")
    category = request.args.get("category", type=int)
    fields_raw = request.args.get("fields")

    fields = None
    if fields_raw:
        fields = fields_raw.split(",")

    body, code = list_books(
        strategy=strategy,
        offset=offset,
        limit=limit,
        cursor=cursor,
        sort=sort,
        genre=genre,
        category_id=category,
        fields=fields,
    )
    return jsonify(body), code


@app.get("/api/v1/books/<int:book_id>")
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(book.to_dict())


@app.get("/api/v1/authors")
def list_authors():
    authors = Author.query.all()
    data = []
    for a in authors:
        data.append(a.to_dict())
    return jsonify({"data": data})


@app.get("/api/v1/authors/<int:author_id>/books")
def author_books(author_id):
    author = Author.query.get(author_id)
    if author is None:
        return jsonify({"error": "not found"}), 404
    books = Book.query.filter(Book.authors.any(id=author_id)).all()
    data = []
    for b in books:
        data.append(b.to_dict())
    return jsonify({"data": data, "author": author.to_dict()})


@app.get("/api/v1/categories")
def list_categories():
    cats = Category.query.all()
    data = []
    for c in cats:
        data.append(c.to_dict())
    return jsonify({"data": data})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
