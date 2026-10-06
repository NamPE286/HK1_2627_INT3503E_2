import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / name / 'app.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
b1, b2, b3 = [load(n) for n in ('b1', 'b2', 'b3')]

@b2.app.get('/test-unhandled')
def crash():
    raise RuntimeError('private-server-detail')

class Labs(unittest.TestCase):
    def test_blog(self):
        b1.posts.clear(); b1.next_post_id = 1
        c = b1.app.test_client()
        r = c.post('/api/v1/posts', json=dict(author_id=1, title=' Hello ', content=' World '))
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.headers['Location'], '/api/v1/posts/1')
        self.assertEqual(r.json['title'], 'Hello')
        self.assertEqual(c.get('/api/v1/posts?author_id=1&size=1').json['pagination']['total'], 1)
        self.assertEqual(c.get('/api/v1/posts?author_id=2').json['data'], [])

    def test_errors(self):
        c = b2.app.test_client()
        self.assertEqual(c.get('/resources/1').status_code, 200)
        for headers in ({}, {'Accept':'application/json'}, {'Accept':'text/html'}):
            r = c.get('/resources/9999', headers=headers)
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.content_type, 'application/problem+json')
            self.assertEqual(r.json['status'], 404)
            self.assertEqual(r.json['instance'], '/resources/9999')
            self.assertEqual(set(r.json), {'type','title','detail','status','instance'})
        self.assertEqual(c.get('/missing').status_code, 404)
        self.assertEqual(c.post('/resources/1').status_code, 405)
        r = c.get('/test-unhandled')
        self.assertEqual(r.status_code, 500)
        self.assertNotIn('private-server-detail', r.get_data(as_text=True))
        self.assertEqual(r.content_type, 'application/problem+json')
        self.assertEqual(r.json['status'], 500)

    def test_cursor_and_sort(self):
        c = b3.app.test_client()
        for sort in ('id', '-id', '-total,customer_id', 'status,-created_at'):
            url = '/orders?limit=3&sort=' + sort
            actual = []
            while url:
                r = c.get(url)
                self.assertEqual(r.status_code, 200)
                actual.extend(r.json['data'])
                url = r.json['pagination']['next']
            terms = sort.split(',')
            if not any(t.removeprefix('-') == 'id' for t in terms): terms.append('id')
            expected = list(b3.orders)
            for term in reversed(terms):
                expected.sort(key=lambda o:o[term.removeprefix('-')], reverse=term.startswith('-'))
            self.assertEqual(actual, expected)
            self.assertEqual(len({o['id'] for o in actual}), 20)

    def test_filters_and_fields(self):
        c = b3.app.test_client()
        r = c.get('/orders?status=paid&customer_id=2&fields=id,total&limit=1&sort=-total')
        self.assertEqual(r.json['data'], [{'id':14,'total':300}])
        self.assertEqual(c.get(r.json['pagination']['next']).json['data'], [{'id':2,'total':200}])
        r = c.get('/orders?customer_id=999')
        self.assertEqual(r.json['data'],[])
        self.assertIsNone(r.json['pagination']['next_cursor'])

    def test_orders_errors(self):
        c = b3.app.test_client()

        queries = (
            "cursor=broken",
            "cursor=",
            "limit=0",
            "limit=101",
            "limit=no",
            "sort=unknown",
            "fields=unknown",
            "fields=unknown&customer_id=999",
            "status=unknown",
            "customer_id=no",
            "customer_id=-1",
        )

        for query in queries:
            with self.subTest(query=query):
                response = c.get("/orders?" + query)
                self.assertEqual(response.status_code, 400)

        response = c.get("/orders?status=paid&limit=1")
        token = response.json["pagination"]["next_cursor"]

        response = c.get("/orders?cursor=" + token)
        self.assertEqual(response.status_code, 400)

        for payload in ({}, [], {"last_id": 999, "context": {
            "status": None, "customer_id": None, "sort": ["id"]
        }}):
            token = b3.signer.dumps(payload)
            self.assertEqual(c.get("/orders?cursor=" + token).status_code, 400)

if __name__ == '__main__': unittest.main()
