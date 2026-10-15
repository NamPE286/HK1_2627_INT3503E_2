from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

book_authors = db.Table(
    "book_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True),
)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    slug = db.Column(db.String(80))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
        }


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    bio = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
        }


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    isbn = db.Column(db.String(13))
    price_vnd = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)
    genre = db.Column(db.String(60))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category")
    authors = db.relationship("Author", secondary=book_authors)

    def to_dict(self, fields=None):
        d = {
            "id": "book_" + str(self.id),
            "title": self.title,
            "isbn": self.isbn,
            "price": {
                "amount": self.price_vnd,
                "currency": "VND",
            },
            "stock": self.stock,
            "genre": self.genre,
            "inStock": self.stock > 0,
            "category": self.category.to_dict() if self.category else None,
            "authors": [{"id": a.id, "name": a.name} for a in self.authors],
        }
        if fields is not None:
            result = {}
            for k in fields:
                if k in d:
                    result[k] = d[k]
            return result
        return d
