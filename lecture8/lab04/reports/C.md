# Kịch bản C — Spike

Locust chạy 200 user, tăng 50 user/giây trong 30 giây.
Cửa sổ đo theo UTC từ `2026-11-16T13:37:17Z` đến `2026-11-16T13:37:47Z`.

| Request | Tổng | Lỗi | Tỷ lệ lỗi | Request/s | p50 (ms) | p95 (ms) | p99 (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `GET /books` | 1240 | 0 | 0,00% | 42,68 | 4 | 30 | 48 |
| `GET /books/{id}` | 808 | 0 | 0,00% | 27,81 | 4 | 25 | 50 |
| `GET /books?year` | 404 | 4 | 0,99% | 13,91 | 4 | 31 | 46 |
| `POST /books` | 383 | 0 | 0,00% | 13,18 | 6 | 31 | 54 |
| **Tổng** | 2835 | 4 | 0,14% | 97,59 | 4 | 30 | 50 |

## Lỗi

- `GET /books?year`: 4 lần `CatchResponseError('Simulated 500 (Locust)')`.
