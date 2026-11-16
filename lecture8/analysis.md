# Phân tích tải Products API

Đo `GET /api/v1/products` trên API Lecture 7. API chạy bằng Gunicorn với 1 worker, 4 thread và SQLite chứa 2 sản phẩm mẫu. Locust chạy cùng máy với API. Mỗi user giả lập nghỉ 1–2 giây giữa hai request và có timeout 5 giây. Thời lượng mỗi kịch bản bao gồm giai đoạn tăng user.

| Kịch bản | User | Tăng user/s | Thời lượng | Request | Request/s | p95 | Tỷ lệ lỗi |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [Baseline](reports/baseline.md) | 10 | 2 | 30 s | 186 | 6,29 | 33 ms | 0/186 (0%) |
| [Normal](reports/normal.md) | 50 | 5 | 60 s | 1.842 | 30,90 | 29 ms | 2/1.842 (0,11%) |
| [Spike](reports/spike.md) | 200 | 50 | 30 s | 3.757 | 128,24 | 120 ms | 10/3.757 (0,27%) |

## Nhận xét

Spike có p95 cao nhất. So với 50 user, thông lượng tăng từ 30,90 lên 128,24 request/s và p95 tăng từ 29 lên 120 ms. Cả 10 lỗi spike tập trung trong khoảng giây thứ 12–13 của bài đo, sau khi đã đạt 200 user. Locust ghi nhận 8 kết nối bị reset và 2 kết nối bị đóng trước khi có HTTP response. Cần đối chiếu log Gunicorn và số kết nối quanh thời điểm phát sinh lỗi để xác định nguyên nhân.

Một lần chạy thăm dò ở mức 50 user cho p95 170 ms và 25 lỗi kết nối trên 1.811 request (1,38%). Mức tải này cần được đo lặp lại vì tỷ lệ lỗi đã dao động qua ngưỡng 1%.

## SLO đề xuất

Ở tải thường 50 user giả lập, giữ **p95 dưới 300 ms** và **tỷ lệ lỗi dưới 1%** trong cửa sổ đo 5 phút. p95 theo dõi nhóm request chậm, còn tỷ lệ lỗi theo dõi cả request lỗi HTTP và lỗi kết nối.

Lần đo chính thức ở mức 50 user đạt hai ngưỡng trong 60 giây. Dùng kịch bản 10 user trong 30 giây làm smoke test cho CI. Trước khi xác nhận SLO, chạy lại kịch bản 50 user trong 5 phút trên staging với lượng dữ liệu gần thực tế và máy phát tải riêng.
