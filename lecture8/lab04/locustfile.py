from random import choice, randint, random

from locust import HttpUser, between, task


class BooksUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_books(self):
        self.client.get("/books", name="GET /books", timeout=5)

    @task(2)
    def read_book(self):
        book_id = randint(1, 50)
        with self.client.get(
            f"/books/{book_id}", name="GET /books/{id}", timeout=5, catch_response=True
        ) as response:
            if response.status_code == 404:
                response.success()

    @task
    def create_book(self):
        self.client.post(
            "/books", json={"title": "Load test", "author": "Locust"},
            name="POST /books", timeout=5,
        )

    @task
    def search_by_year(self):
        with self.client.get(
            "/books", params={"year": choice((2017, 2021, 2025))},
            name="GET /books?year", timeout=5, catch_response=True,
        ) as response:
            if response.ok and random() < 0.01:
                response.failure("Simulated 500 (Locust)")
