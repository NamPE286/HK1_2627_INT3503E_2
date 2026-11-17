# Lab 4 — Đo tải Books API bằng Locust

Locust chạy các thao tác liệt kê, đọc, tạo sách và tìm theo năm. Bài đo dùng Flask development server và SQLite trên cùng máy với Locust. Mỗi kịch bản bắt đầu với một cơ sở dữ liệu tạm chứa cùng 50 sách mẫu. Mỗi user đợi 1–3 giây giữa các task.

Task tìm theo năm đánh dấu khoảng 1% response thành công thành lỗi bằng `response.failure()`. Đây là lỗi mô phỏng phía Locust. Flask vẫn trả status gốc. Khi đọc sách bằng ID ngẫu nhiên, `404` là kết quả dự kiến nếu ID vắng mặt.

Từ `lecture8/lab04`, cài phụ thuộc và chạy Books API có dữ liệu mẫu.

```sh
python -m pip install -r ../lab01/requirements.txt -r requirements.txt
PYTHONPATH=../lab01 python - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory

from app import create_app
from models import Book, db

with TemporaryDirectory() as directory:
    database = Path(directory, "books.db")
    app = create_app({"SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}"})
    with app.app_context():
        for number in range(1, 51):
            year = (2017, 2021, 2025)[number % 3]
            db.session.add(Book(title=f"Book {number}", author="Seed", year=year))
        db.session.commit()
    app.run()
PY
```

Mở terminal khác tại `lecture8/lab04`. Khởi động lại API bằng lệnh trên trước mỗi kịch bản để đặt lại dữ liệu. Locust vẫn xuất báo cáo khi có request lỗi.

```sh
locust -f locustfile.py --headless -H http://127.0.0.1:5000 -u 10 -r 2 -t 30s --html reports/A.html
locust -f locustfile.py --headless -H http://127.0.0.1:5000 -u 50 -r 5 -t 60s --html reports/B.html
locust -f locustfile.py --headless -H http://127.0.0.1:5000 -u 200 -r 50 -t 30s --html reports/C.html
```

Các file HTML là báo cáo Locust xuất từ ba lần chạy Books API. [Phân tích và báo cáo từng kịch bản](analysis.md)

Ảnh đầu ra Locust của từng kịch bản:

- [A — Baseline](evidence/A-terminal.png)
- [B — Tải thường](evidence/B-terminal.png)
- [C — Spike](evidence/C-terminal.png)
