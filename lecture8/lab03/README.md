# Lab 3 — Postman và Newman

Collection giữ năm request CRUD của starter. Request tạo lưu `book_id` để các request đọc, sửa và xóa dùng lại. Folder `error-cases` kiểm tra status và JSON của hai ca lỗi.

| Request | Status | Mã lỗi |
| --- | --- | --- |
| `POST /books` thiếu `title` | 400 | `VALIDATION_ERROR` |
| `GET /books/9999` | 404 | `NOT_FOUND` |

Từ `lecture8/lab01`, cài phụ thuộc và chạy Books API cục bộ.

```sh
python -m pip install -r requirements.txt
mkdir -p instance
python -m app --port 5000
```

Mở terminal khác tại `lecture8/lab03` và chạy Newman. Dùng cơ sở dữ liệu dành cho bài lab với ID 9999 chưa được dùng.

```sh
npx --yes newman@6.2.1 run books-api.postman_collection.json \
  -e local.postman_environment.json --timeout-request 5000 \
  -r cli,junit --reporter-junit-export junit.xml
```

Lần chạy đã lưu có 7 request và 14 assertion, tất cả đều pass trong 101 ms. [Báo cáo JUnit](junit.xml)

[Ảnh đầu ra Newman](evidence/newman-terminal.png)
