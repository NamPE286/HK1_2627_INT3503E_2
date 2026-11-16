# Báo cáo Locust — Spike

Đo `GET /api/v1/products` tại `http://127.0.0.1:5000` bằng `locustfile.py`.

- Cấu hình tải gồm 200 user, tăng 50 user/giây, chạy 30 giây.
- Cửa sổ đo theo UTC từ `2026-11-11T06:01:20Z` đến `2026-11-11T06:01:49Z`.

## Kết quả

| Request | Lỗi | Tỷ lệ lỗi | Request/s | Min (ms) | TB (ms) | Max (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 3757 | 10 | 0.27% | 128.24 | 2 | 16.57 | 300 |

## Phân vị thời gian phản hồi

| p50 (ms) | p60 (ms) | p70 (ms) | p80 (ms) | p90 (ms) | p95 (ms) | p99 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 5 | 7 | 9 | 23 | 120 | 190 |

## Lỗi

| Lỗi | Số lần | Đầu tiên (UTC) | Cuối cùng (UTC) |
| --- | --- | --- | --- |
| `RemoteDisconnected('Remote end closed connection without response')` | 2 | 06:01:32 | 06:01:32 |
| `ConnectionResetError(104, 'Connection reset by peer')` | 8 | 06:01:32 | 06:01:33 |

## Lịch sử tải

| Giây từ lúc bắt đầu | User | Request/s | Lỗi/s | TB (ms) | p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 200 | 73.33 | 0.00 | 49.88 | 10 | 140 |
| 10 | 200 | 110.88 | 0.00 | 25.09 | 5 | 130 |
| 15 | 200 | 131.10 | 0.90 | 28.51 | 5 | 140 |
| 20 | 200 | 130.20 | 1.00 | 22.44 | 5 | 150 |
| 25 | 200 | 131.60 | 0.10 | 18.66 | 4 | 9 |
| 29 | 0 | 132.60 | 0.00 | 16.57 | 4 | 10 |
