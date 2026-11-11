def test_list_books_returns_empty_array(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_missing_book_returns_not_found(client):
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_without_title_reports_validation_error(client):
    response = client.post("/books", json={"author": "J.J. Geewax"})

    assert response.status_code == 400
    assert any(error["field"] == "title" for error in response.get_json()["errors"])


def test_deleted_book_can_no_longer_be_retrieved(client):
    created = client.post("/books", json={"title": "API Design Patterns", "author": "J.J. Geewax"})
    assert created.status_code == 201
    path = f"/books/{created.get_json()['id']}"

    assert client.delete(path).status_code == 204
    assert client.get(path).status_code == 404
