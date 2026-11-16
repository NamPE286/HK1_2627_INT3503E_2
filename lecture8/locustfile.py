from locust import HttpUser, between, task


class ProductsUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def list_products(self):
        with self.client.get(
            "/api/v1/products", timeout=5, catch_response=True
        ) as response:
            if response.status_code == 0:
                return
            if response.status_code != 200:
                response.failure(f"Expected HTTP 200, got {response.status_code}")
                return
            try:
                products = response.json()
            except ValueError:
                response.failure("Invalid JSON")
                return
            if not isinstance(products, list):
                response.failure("Expected a list of products")
