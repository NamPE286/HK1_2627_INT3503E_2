"""Tests for the Lecture 2 Books API.

Run with: python -m unittest discover -s lecture2 -v
"""

import unittest
from unittest.mock import patch

import app as lecture_app


class BooksAPITestCase(unittest.TestCase):
    def setUp(self):
        self.seed_books = [
            {"id": 1, "title": "Clean Code", "author": "Robert Martin"},
            {"id": 2, "title": "The Clean Coder", "author": "Robert Martin"},
            {"id": 3, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"},
        ]

        books_patcher = patch.object(
            lecture_app, "books", [book.copy() for book in self.seed_books]
        )
        id_patcher = patch.object(lecture_app, "next_id", 4)
        config_patcher = patch.dict(lecture_app.app.config, TESTING=True)

        books_patcher.start()
        id_patcher.start()
        config_patcher.start()
        self.addCleanup(books_patcher.stop)
        self.addCleanup(id_patcher.stop)
        self.addCleanup(config_patcher.stop)

        self.client = lecture_app.app.test_client()

    def create_book(self, title="Fluent Python", author="Luciano Ramalho"):
        return self.client.post(
            "/books", json={"title": title, "author": author}
        )

    def test_list_books_has_pagination_links_and_cache_header(self):
        response = self.client.get("/books")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Cache-Control"], "public, max-age=30")
        self.assertEqual(response.get_json(), {
            "data": self.seed_books,
            "pagination": {
                "page": 1,
                "size": 20,
                "total": 3,
                "total_pages": 1,
            },
            "_links": {
                "self": {"href": "/books?page=1&size=20"},
                "first": {"href": "/books?page=1&size=20"},
                "last": {"href": "/books?page=1&size=20"},
            },
        })

    def test_list_books_paginates_and_exposes_navigation_links(self):
        first_page = self.client.get("/books?page=1&size=2").get_json()
        second_page = self.client.get("/books?page=2&size=2").get_json()

        self.assertEqual(first_page["data"], self.seed_books[:2])
        self.assertEqual(first_page["pagination"], {
            "page": 1, "size": 2, "total": 3, "total_pages": 2,
        })
        self.assertNotIn("prev", first_page["_links"])
        self.assertEqual(
            first_page["_links"]["next"], {"href": "/books?page=2&size=2"}
        )

        self.assertEqual(second_page["data"], self.seed_books[2:])
        self.assertNotIn("next", second_page["_links"])
        self.assertEqual(
            second_page["_links"]["prev"], {"href": "/books?page=1&size=2"}
        )

    def test_pagination_values_are_bounded(self):
        response = self.client.get("/books?page=0&size=500")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["pagination"]["page"], 1)
        self.assertEqual(payload["pagination"]["size"], 100)

    def test_invalid_pagination_returns_400(self):
        for query in ({"page": "one"}, {"size": "many"}, {"page": "1.5"}):
            with self.subTest(query=query):
                response = self.client.get("/books", query_string=query)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(), {"error": "page and size must be int"}
                )

    def test_empty_collection_has_zero_total_pages(self):
        lecture_app.books.clear()

        payload = self.client.get("/books").get_json()

        self.assertEqual(payload["data"], [])
        self.assertEqual(payload["pagination"]["total"], 0)
        self.assertEqual(payload["pagination"]["total_pages"], 0)

    def test_filter_by_author_is_case_insensitive(self):
        response = self.client.get(
            "/books", query_string={"author": "robert martin"}
        )

        payload = response.get_json()
        self.assertEqual(payload["data"], self.seed_books[:2])
        self.assertEqual(payload["pagination"]["total"], 2)

    def test_search_title_is_case_insensitive_and_combines_with_author(self):
        response = self.client.get(
            "/books",
            query_string={"q": "CLEAN CODER", "author": "ROBERT MARTIN"},
        )

        payload = response.get_json()
        self.assertEqual(payload["data"], [self.seed_books[1]])
        self.assertEqual(payload["pagination"]["total"], 1)

    def test_get_book_has_cache_header(self):
        response = self.client.get("/books/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.seed_books[0])
        self.assertEqual(response.headers["Cache-Control"], "max-age=60")

    def test_create_book_returns_location_and_trims_text(self):
        response = self.client.post(
            "/books", json={"title": "  Fluent Python ", "author": " Ramalho  "}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "id": 4, "title": "Fluent Python", "author": "Ramalho",
        })
        self.assertEqual(response.headers["Location"], "/books/4")
        self.assertEqual(self.client.get("/books/4").get_json(), response.get_json())

    def test_create_requires_non_blank_title_and_author(self):
        invalid_bodies = (
            {},
            {"title": "A title"},
            {"author": "An author"},
            {"title": "   ", "author": "An author"},
            {"title": "A title", "author": None},
        )

        for body in invalid_bodies:
            with self.subTest(body=body):
                response = self.client.post("/books", json=body)
                self.assertEqual(response.status_code, 422)
                self.assertEqual(
                    response.get_json(), {"error": "title and author required"}
                )
        self.assertEqual(lecture_app.books, self.seed_books)

    def test_replace_book_requires_both_fields_and_replaces_resource(self):
        invalid = self.client.put("/books/1", json={"title": "Only a title"})
        self.assertEqual(invalid.status_code, 422)
        self.assertEqual(lecture_app.books[0], self.seed_books[0])

        response = self.client.put(
            "/books/1",
            json={
                "title": "Refactoring",
                "author": "Martin Fowler",
                "isbn": "978-0134757599",
                "price": 42,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "id": 1,
            "title": "Refactoring",
            "author": "Martin Fowler",
            "isbn": "978-0134757599",
            "price": 42,
        })

    def test_patch_updates_only_supplied_fields(self):
        response = self.client.patch(
            "/books/1", json={"title": "Clean Code, Second Edition", "price": 35}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            **self.seed_books[0],
            "title": "Clean Code, Second Edition",
            "price": 35,
        })

    def test_patch_rejects_negative_price_without_changing_book(self):
        response = self.client.patch("/books/1", json={"price": -1})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json(), {"error": "price must be positive"})
        self.assertEqual(lecture_app.books[0], self.seed_books[0])

    def test_missing_book_returns_404_for_all_item_operations(self):
        for method in ("GET", "PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                response = self.client.open(
                    "/books/999",
                    method=method,
                    json={"title": "Title", "author": "Author"},
                )
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.get_json(), {"error": "not found"})

    def test_delete_book_returns_204_and_removes_it(self):
        response = self.client.delete("/books/2")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.client.get("/books/2").status_code, 404)
        self.assertEqual(
            self.client.get("/books").get_json()["data"],
            [self.seed_books[0], self.seed_books[2]],
        )

    def test_ids_are_not_reused_after_deletion(self):
        first = self.create_book().get_json()
        self.client.delete(f"/books/{first['id']}")
        second = self.create_book("Python Distilled", "David Beazley").get_json()

        self.assertGreater(second["id"], first["id"])


if __name__ == "__main__":
    unittest.main()
