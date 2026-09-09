from flask import Flask, request

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return {"you sent": data}

@app.get("/")
def index():
    return {"message": "Hello, API!"}
