# Kịch bản B — Tải thường

Locust chạy 50 user, tăng 5 user/giây trong 60 giây.
Cửa sổ đo theo UTC từ `2026-11-16T13:36:16Z` đến `2026-11-16T13:37:16Z`.

| Request | Tổng | Lỗi | Tỷ lệ lỗi | Request/s | p50 (ms) | p95 (ms) | p99 (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `GET /books` | 590 | 0 | 0,00% | 9,97 | 5 | 9 | 14 |
| `GET /books/{id}` | 395 | 0 | 0,00% | 6,67 | 5 | 9 | 15 |
| `GET /books?year` | 209 | 3 | 1,44% | 3,53 | 5 | 8 | 14 |
| `POST /books` | 192 | 0 | 0,00% | 3,24 | 7 | 11 | 20 |
| **Tổng** | 1386 | 3 | 0,22% | 23,42 | 5 | 9 | 15 |

## Lỗi

- `GET /books?year`: 3 lần `CatchResponseError('Simulated 500 (Locust)')`.
