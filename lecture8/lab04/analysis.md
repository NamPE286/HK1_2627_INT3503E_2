# Phân tích tải Books API

| Kịch bản | User | Tăng user/s | Thời lượng | Request | Request/s | p95 (ms) | Lỗi |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [A — Baseline](reports/A.md) | 10 | 2 | 30 s | 142 | 4,88 | 9 | 0/142 (0,00%) |
| [B — Tải thường](reports/B.md) | 50 | 5 | 60 s | 1.386 | 23,42 | 9 | 3/1.386 (0,22%) |
| [C — Spike](reports/C.md) | 200 | 50 | 30 s | 2.835 | 97,59 | 30 | 4/2.835 (0,14%) |

Spike có p95 cao nhất. Từ 50 lên 200 user, thông lượng tăng từ 23,42 lên 97,59 request/s và p95 tăng từ 9 lên 30 ms. p95 của cả bốn nhóm request đều tăng. Flask xử lý nhiều request đồng thời hơn và các request ghi dùng chung một file SQLite, nên thời gian chờ là một khả năng. Cần đo thời gian chờ ở Flask và SQLite để xác định nguyên nhân.

`GET /books?year` ghi nhận 0/16, 3/209 (1,44%) và 4/404 (0,99%) lỗi ở A, B và C. Tỷ lệ này dao động theo việc Locust đánh dấu ngẫu nhiên 1% response thành công là lỗi mô phỏng. Cả ba lượt đo ghi nhận 0 lỗi thực.

Cả ba kịch bản đạt ngưỡng giả định p95 dưới 300 ms trong bài đo cục bộ. Dùng A (10 user, 30 giây) làm smoke test cho CI, với p95 dưới 300 ms và 0 lỗi thực. Khi tính lỗi thực, loại riêng các lỗi mang nhãn `Simulated 500 (Locust)`. Đo lại trên staging trước khi dùng kết quả để đánh giá SLO production.

Nếu pool giới hạn 5 kết nối và không cho mở thêm, request cần kết nối thứ sáu phải chờ. Khi chờ quá timeout, request có thể lỗi. Để kiểm tra, chạy lại C với cùng dữ liệu, so sánh pool mặc định với `pool_size=5` và `max_overflow=0`, rồi đối chiếu p95, số lỗi và thời gian chờ lấy kết nối.
