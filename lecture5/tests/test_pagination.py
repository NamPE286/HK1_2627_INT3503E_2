import pytest
from app import app, db, seed


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    # reset flag
    import app as app_module
    app_module._ready = False
    with app.app_context():
        db.create_all()
        seed()
        with app.test_client() as c:
            yield c
        db.drop_all()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200


def test_list_books(client):
    r = client.get("/api/v1/books")
    assert r.status_code == 200
    assert "data" in r.json
    assert "pagination" in r.json
    assert len(r.json["data"]) == 8


def test_limit(client):
    r = client.get("/api/v1/books?limit=3")
    assert r.status_code == 200
    assert len(r.json["data"]) == 3
    assert r.json["pagination"]["has_more"] == True


def test_offset(client):
    r = client.get("/api/v1/books?strategy=offset&offset=0&limit=3")
    assert r.status_code == 200
    assert r.json["pagination"]["strategy"] == "offset"
    assert r.json["pagination"]["total"] == 8


def test_cursor(client):
    r1 = client.get("/api/v1/books?limit=3&sort=-id")
    assert r1.status_code == 200
    cursor = r1.json["pagination"]["next_cursor"]
    assert cursor is not None

    r2 = client.get("/api/v1/books?limit=3&sort=-id&cursor=" + cursor)
    assert r2.status_code == 200
    ids1 = [b["id"] for b in r1.json["data"]]
    ids2 = [b["id"] for b in r2.json["data"]]
    for x in ids1:
        assert x not in ids2


def test_genre(client):
    r = client.get("/api/v1/books?genre=tech")
    assert r.status_code == 200
    for b in r.json["data"]:
        assert b["genre"] == "tech"


def test_sort(client):
    r = client.get("/api/v1/books?sort=-price&limit=5")
    assert r.status_code == 200
    prices = []
    for b in r.json["data"]:
        prices.append(b["price"]["amount"])
    assert prices == sorted(prices, reverse=True)


def test_bad_sort(client):
    r = client.get("/api/v1/books?sort=xyz")
    assert r.status_code == 400
