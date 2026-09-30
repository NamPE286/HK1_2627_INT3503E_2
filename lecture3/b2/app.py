from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


class ProblemError(Exception):
    def __init__(self, status, title, detail):
        self.status, self.title, self.detail = status, title, detail


def problem(status, title, detail):
    response = jsonify(type="about:blank", title=title, detail=detail,
                       status=status, instance=request.path)
    response.content_type = "application/problem+json"
    return response, status


@app.errorhandler(ProblemError)
def handle_problem(error):
    return problem(error.status, error.title, error.detail)


@app.errorhandler(HTTPException)
def handle_http(error):
    return problem(error.code, error.name, error.description)


@app.errorhandler(Exception)
def handle_unexpected(error):
    app.logger.exception("Unhandled error")
    return problem(500, "Internal Server Error", "An unexpected error occurred.")


@app.get("/resources/<int:resource_id>")
def get_resource(resource_id):
    if resource_id != 1:
        raise ProblemError(404, "Not Found", "Resource not found.")
    return {"id": 1, "name": "Example resource"}


if __name__ == "__main__":
    app.run()
