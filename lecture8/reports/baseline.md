# Báo cáo Locust — Baseline

Đo `GET /api/v1/products` tại `http://127.0.0.1:5000` bằng `locustfile.py`.

- Cấu hình tải gồm 10 user, tăng 2 user/giây, chạy 30 giây.
- Cửa sổ đo theo UTC từ `2026-11-11T05:59:48Z` đến `2026-11-11T06:00:18Z`.

## Kết quả

| Request | Lỗi | Tỷ lệ lỗi | Request/s | Min (ms) | TB (ms) | Max (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 186 | 0 | 0.00% | 6.29 | 3 | 11.00 | 232 |

## Phân vị thời gian phản hồi

| p50 (ms) | p60 (ms) | p70 (ms) | p80 (ms) | p90 (ms) | p95 (ms) | p99 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 7 | 8 | 10 | 18 | 33 | 200 |

## Lỗi

Locust ghi nhận 0 request lỗi.

## Lịch sử tải

| Giây từ lúc bắt đầu | User | Request/s | Lỗi/s | TB (ms) | p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 10 | 2.67 | 0.00 | 7.07 | 5 | 8 |
| 10 | 10 | 5.00 | 0.00 | 6.80 | 5 | 13 |
| 15 | 10 | 6.70 | 0.00 | 15.55 | 8 | 62 |
| 20 | 10 | 6.80 | 0.00 | 12.97 | 7 | 62 |
| 25 | 10 | 6.50 | 0.00 | 11.60 | 4 | 12 |
| 30 | 0 | 6.40 | 0.00 | 11.00 | 5 | 33 |
