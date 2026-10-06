from flask import Flask, abort, request, url_for
from itsdangerous import BadData, URLSafeSerializer


app = Flask(__name__)

signer = URLSafeSerializer("lecture3-local-demo", salt="orders-v1")

orders = []
statuses = ["pending", "paid", "shipped"]

for i in range(1, 21):
    order = {
        "id": i,
        "customer_id": (i - 1) % 4 + 1,
        "status": statuses[(i - 1) % 3],
        "total": 100 + (i % 5) * 50,
        "created_at": f"2026-10-{i:02d}T08:00:00Z",
    }

    orders.append(order)


@app.errorhandler(BadData)
@app.errorhandler(ValueError)
def invalid_input(error):
    return {"error": "Invalid cursor or query parameter."}, 400


@app.get("/orders")
def list_orders():
    limit = int(request.args.get("limit", 5))
    status = request.args.get("status")
    customer_id = request.args.get("customer_id")

    sort = request.args.get("sort", "id").split(",")
    fields = request.args.get("fields")
    cursor = request.args.get("cursor")

    if limit < 1 or limit > 100:
        abort(400, description="limit must be between 1 and 100.")

    if status is not None and status not in statuses:
        abort(400, description="Unknown status.")

    available_fields = set(orders[0])

    if fields is not None:
        selected_fields = fields.split(",")

        if any(field not in available_fields for field in selected_fields):
            abort(400, description="Unknown field.")

    data = orders.copy()

    if status is not None:
        data = [order for order in data if order["status"] == status]

    if customer_id is not None:
        customer_id = int(customer_id)

        if customer_id < 1:
            abort(400, description="customer_id must be positive.")

        data = [order for order in data if order["customer_id"] == customer_id]

    sort_fields = [field.lstrip("-") for field in sort]

    if any(field not in available_fields for field in sort_fields):
        abort(400, description="Unknown sort field.")

    if "id" not in sort_fields:
        sort.append("id")

    for field in reversed(sort):
        name = field.lstrip("-")
        descending = field.startswith("-")

        data.sort(key=lambda order: order[name], reverse=descending)

    context = {
        "status": status,
        "customer_id": customer_id,
        "sort": sort,
    }

    if cursor is not None:
        payload = signer.loads(cursor)
        if not isinstance(payload, dict) or payload.get("context") != context:
            abort(400, description="Cursor does not match filters or sort.")

        last_id = payload.get("last_id")

        start = next(
            (i for i, order in enumerate(data) if order["id"] == last_id),
            None,
        )

        if start is None:
            abort(400, description="Invalid cursor.")

        data = data[start + 1 :]

    page = data[:limit]

    next_cursor = None
    next_url = None

    if len(data) > limit:
        next_cursor = signer.dumps({
            "last_id": page[-1]["id"],
            "context": context,
        })

        params = request.args.to_dict()
        params["cursor"] = next_cursor

        next_url = url_for("list_orders", **params)

    if fields is not None:
        result = []

        for order in page:
            item = {field: order[field] for field in selected_fields}
            result.append(item)

        page = result

    return {
        "data": page,
        "pagination": {
            "limit": limit,
            "has_more": next_cursor is not None,
            "next_cursor": next_cursor,
            "next": next_url,
        },
    }
