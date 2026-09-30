from flask import Flask, request


app = Flask(__name__)
posts = []
next_post_id = 1


@app.get("/api/v1/posts")
def list_posts():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 20))
    author_id = request.args.get("author_id")

    data = posts
    if author_id is not None:
        data = [post for post in data if post["author_id"] == int(author_id)]

    total = len(data)
    start = (page - 1) * size

    return {
        "data": data[start : start + size],
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": (total + size - 1) // size,
        },
    }


@app.post("/api/v1/posts")
def create_post():
    global next_post_id

    data = request.get_json()

    post = {
        "id": next_post_id,
        "author_id": data["author_id"],
        "title": data["title"].strip(),
        "content": data["content"].strip(),
    }
    posts.append(post)
    next_post_id += 1

    return post, 201, {"Location": f"/api/v1/posts/{post['id']}"}


if __name__ == "__main__":
    app.run(debug=True)
