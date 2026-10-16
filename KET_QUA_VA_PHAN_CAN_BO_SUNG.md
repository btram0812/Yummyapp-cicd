# Kết quả thực chạy và phần cần bổ sung

## Đã thực hiện

- Khôi phục ba file Python từ mã khởi tạo và hoàn thiện bộ test.
- 14 test chạy thành công; flake8 theo bộ chọn của đề: 0 lỗi.
- Coverage tổng: 98% (87/89 dòng); riêng yummy_app.py: 100% (30/30 dòng).
- Quality Gate 80%: mã thoát 0, Pass.
- Có log thực trong logs/local_test.log và báo cáo HTML trong coverage_html/index.html.
- Có workflow Ubuntu/Python 3.11, push và pull_request vào main, upload artifact giữ 7 ngày.
- Có sơ đồ, ma trận bảy ca, sáu câu trả lời và hướng dẫn thực hiện trong LOI_GIAI_LAB7.md.

Môi trường thực chạy local: Windows, CPython 3.12.14; coverage 7.4.0, flake8 7.0.0, requests 2.31.0. Chưa chạy xác nhận trên Python 3.11/Ubuntu; đó là môi trường được cấu hình trong CI. Hai dòng chưa chạy là hàm GPS thật bị mock và unittest.main() khi dùng discover, không phải nhánh nghiệp vụ bị bỏ sót.

## Chưa có bằng chứng để hoàn tất bản nộp

1. Họ tên, MSSV, email và repository GitHub công khai của sinh viên.
2. Lịch sử commit thật có định danh sinh viên: logs/git_history.log.
3. Các lần chạy GitHub Actions theo trình tự yêu cầu, ảnh chụp và raw log cuối: logs/github_actions_run.log.
4. Bốn trang viết tay có định danh, ngày thực hành, chữ ký; scan thành MinhChung_VietTay_MSSV.pdf.
5. BaoCao_KetQua_Lab7.pdf có link repository, ảnh và kết quả run thật.

ZIP đi kèm là bộ bài giải để tiếp tục thực hành, chưa phải bộ minh chứng nộp hoàn chỉnh. Không tạo log GitHub, chữ ký hoặc lịch sử commit giả.
