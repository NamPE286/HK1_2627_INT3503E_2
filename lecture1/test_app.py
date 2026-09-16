"""Books API tests. Run: python -m unittest discover -s lesson1 -v."""

import unittest
from unittest.mock import patch

import app as lesson_app


class BooksAPITestCase(unittest.TestCase):
    def setUp(self):
        # Give each test fresh data and restore the application state afterward.
        self.seed = {"id": 1, "title": "Clean Code", "author": "R. Martin"}
        for name, value in (("BOOKS", [self.seed.copy()]), ("_next", 2)):
            patcher = patch.object(lesson_app, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        config = patch.dict(lesson_app.app.config, TESTING=True)
        config.start()
        self.addCleanup(config.stop)
        self.client = lesson_app.app.test_client()

    def create_book(self):
        return self.client.post(
            "/books", json={"title": "DDIA", "author": "Kleppmann"}
        )

    def test_list_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.get_json(), [self.seed])

    def test_list_empty_collection(self):
        self.client.delete("/books/1")
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_list_limit(self):
        self.create_book()
        for limit, expected_count in ((0, 0), (1, 1), (2, 2), (100, 2)):
            with self.subTest(limit=limit):
                response = self.client.get(f"/books?limit={limit}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.get_json()), expected_count)
                if expected_count:
                    self.assertEqual(response.get_json()[0], self.seed)

    def test_invalid_limit(self):
        for limit in ("abc", "-1", "1.5", ""):
            with self.subTest(limit=limit):
                response = self.client.get("/books", query_string={"limit": limit})
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_get_book(self):
        response = self.client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.seed)

    def test_missing_book(self):
        for method in ("GET", "PUT", "DELETE"):
            with self.subTest(method=method):
                response = self.client.open("/books/999", method=method)
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.get_json(), {"error": "not found"})
        self.assertEqual(self.client.get("/books").get_json(), [self.seed])

    def test_create_book_and_location(self):
        response = self.create_book()
        self.assertEqual(response.status_code, 201)
        book = response.get_json()
        self.assertIsInstance(book["id"], int)
        self.assertNotEqual(book["id"], self.seed["id"])
        self.assertEqual(book["title"], "DDIA")
        self.assertEqual(book["author"], "Kleppmann")
        self.assertEqual(response.headers["Location"], f"/books/{book['id']}")
        detail = self.client.get(response.headers["Location"])
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.get_json(), book)
        self.assertEqual(self.client.get("/books").get_json(), [self.seed, book])

    def test_create_requires_title_and_author(self):
        for body in (
            {}, {"title": "DDIA"}, {"author": "Kleppmann"},
            {"title": "", "author": "Kleppmann"},
            {"title": "DDIA", "author": ""},
            {"title": None, "author": "Kleppmann"},
        ):
            with self.subTest(body=body):
                response = self.client.post("/books", json=body)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())
                self.assertEqual(self.client.get("/books").get_json(), [self.seed])

    def test_update_title_preserves_other_fields(self):
        response = self.client.put("/books/1", json={"title": "CC 2nd ed."})
        expected = {**self.seed, "title": "CC 2nd ed."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected)
        self.assertEqual(self.client.get("/books/1").get_json(), expected)

    def test_update_title_and_author(self):
        response = self.client.put(
            "/books/1", json={"title": "New title", "author": "New author"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "id": 1, "title": "New title", "author": "New author",
        })

    def test_delete_has_empty_body_and_removes_book(self):
        created = self.create_book().get_json()
        response = self.client.delete(f"/books/{created['id']}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.client.get(f"/books/{created['id']}").status_code, 404)
        self.assertEqual(self.client.delete(f"/books/{created['id']}").status_code, 404)
        self.assertEqual(self.client.get("/books").get_json(), [self.seed])

    def test_ids_are_not_reused_after_deletion(self):
        first = self.create_book().get_json()
        self.client.delete(f"/books/{first['id']}")
        second = self.create_book().get_json()
        self.assertGreater(second["id"], first["id"])


if __name__ == "__main__":
    unittest.main()
