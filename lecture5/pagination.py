import base64
import json
from sqlalchemy import tuple_
from models import Book

SORT_COLS = {
    "id": Book.id,
    "price": Book.price_vnd,
    "title": Book.title,
    "stock": Book.stock,
}

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def encode_cursor(obj):
    raw = json.dumps(obj)
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def decode_cursor(token):
    pad = 4 - len(token) % 4
    if pad != 4:
        token = token + ("=" * pad)
    return json.loads(base64.urlsafe_b64decode(token))


def parse_sort(raw):
    # vd: -price,title
    if raw is None or raw == "":
        raw = "-id"

    order = []
    main_key = None
    main_desc = False

    parts = raw.split(",")
    for p in parts:
        p = p.strip()
        desc = False
        if p.startswith("-"):
            desc = True
            p = p[1:]
        if p not in SORT_COLS:
            return None, None, None
        col = SORT_COLS[p]
        if desc:
            order.append(col.desc())
        else:
            order.append(col.asc())
        if main_key is None:
            main_key = p
            main_desc = desc

    # them id de tranh trung
    if main_key != "id":
        if main_desc:
            order.append(Book.id.desc())
        else:
            order.append(Book.id.asc())

    return order, main_key, main_desc


def list_books(strategy="cursor", offset=0, limit=20, cursor=None,
               sort=None, genre=None, category_id=None, fields=None):
    if limit < 1:
        limit = 1
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    order, sort_key, desc = parse_sort(sort)
    if order is None:
        return {"error": "invalid sort"}, 400

    q = Book.query.order_by(*order)

    if genre:
        q = q.filter(Book.genre == genre)
    if category_id is not None:
        q = q.filter(Book.category_id == category_id)

    if strategy == "offset":
        total = q.count()
        items = q.offset(offset).limit(limit).all()
        page = {
            "strategy": "offset",
            "offset": offset,
            "limit": limit,
            "total": total,
            "has_more": (offset + limit) < total,
        }
    else:
        # cursor
        if cursor:
            state = decode_cursor(cursor)
            if state.get("s") != sort_key:
                return {"error": "sort changed"}, 400
            v = state["v"]
            i = state["i"]
            col = SORT_COLS[sort_key]
            if desc:
                q = q.filter(tuple_(col, Book.id) < tuple_(v, i))
            else:
                q = q.filter(tuple_(col, Book.id) > tuple_(v, i))

        rows = q.limit(limit + 1).all()
        has_more = len(rows) > limit
        items = rows[:limit]

        next_cursor = None
        if has_more and len(items) > 0:
            last = items[-1]
            val = getattr(last, SORT_COLS[sort_key].key)
            next_cursor = encode_cursor({"s": sort_key, "v": val, "i": last.id})

        page = {
            "strategy": "cursor",
            "next_cursor": next_cursor,
            "has_more": has_more,
            "limit": limit,
        }

    data = []
    for b in items:
        data.append(b.to_dict(fields))

    return {"data": data, "pagination": page}, 200
