# Kịch bản A — Baseline

Locust chạy 10 user, tăng 2 user/giây trong 30 giây.
Cửa sổ đo theo UTC từ `2026-11-16T13:35:46Z` đến `2026-11-16T13:36:15Z`.

| Request | Tổng | Lỗi | Tỷ lệ lỗi | Request/s | p50 (ms) | p95 (ms) | p99 (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `GET /books` | 61 | 0 | 0,00% | 2,09 | 6 | 7 | 11 |
| `GET /books/{id}` | 40 | 0 | 0,00% | 1,37 | 6 | 7 | 9 |
| `GET /books?year` | 16 | 0 | 0,00% | 0,55 | 6 | 8 | 8 |
| `POST /books` | 25 | 0 | 0,00% | 0,86 | 8 | 10 | 14 |
| **Tổng** | 142 | 0 | 0,00% | 4,88 | 6 | 9 | 11 |

## Lỗi

Locust ghi nhận 0 request lỗi.
