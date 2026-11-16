# Báo cáo Locust — Normal

Đo `GET /api/v1/products` tại `http://127.0.0.1:5000` bằng `locustfile.py`.

- Cấu hình tải gồm 50 user, tăng 5 user/giây, chạy 60 giây.
- Cửa sổ đo theo UTC từ `2026-11-11T06:00:19Z` đến `2026-11-11T06:01:18Z`.

## Kết quả

| Request | Lỗi | Tỷ lệ lỗi | Request/s | Min (ms) | TB (ms) | Max (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 1842 | 2 | 0.11% | 30.90 | 2 | 9.34 | 165 |

## Phân vị thời gian phản hồi

| p50 (ms) | p60 (ms) | p70 (ms) | p80 (ms) | p90 (ms) | p95 (ms) | p99 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 7 | 9 | 11 | 17 | 29 | 54 |

## Lỗi

| Lỗi | Số lần | Đầu tiên (UTC) | Cuối cùng (UTC) |
| --- | --- | --- | --- |
| `RemoteDisconnected('Remote end closed connection without response')` | 1 | 06:00:30 | 06:00:30 |
| `ConnectionResetError(104, 'Connection reset by peer')` | 1 | 06:00:56 | 06:00:56 |

## Lịch sử tải

| Giây từ lúc bắt đầu | User | Request/s | Lỗi/s | TB (ms) | p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 25 | 7.50 | 0.00 | 10.64 | 6 | 23 |
| 10 | 50 | 17.25 | 0.00 | 11.91 | 6 | 43 |
| 15 | 50 | 28.00 | 0.10 | 10.33 | 6 | 42 |
| 20 | 50 | 33.30 | 0.10 | 9.10 | 5 | 22 |
| 25 | 50 | 33.20 | 0.00 | 8.04 | 4 | 12 |
| 30 | 50 | 33.10 | 0.00 | 8.37 | 5 | 16 |
| 35 | 50 | 32.80 | 0.00 | 8.63 | 6 | 37 |
| 40 | 50 | 33.00 | 0.10 | 8.90 | 6 | 34 |
| 45 | 50 | 33.30 | 0.10 | 8.84 | 6 | 25 |
| 50 | 50 | 32.80 | 0.00 | 8.99 | 6 | 29 |
| 55 | 50 | 32.80 | 0.00 | 9.15 | 8 | 28 |
| 59 | 0 | 32.40 | 0.00 | 9.34 | 8 | 33 |
