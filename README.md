# YummyApp CI/CD - Lab 7

Backend Python mô phỏng đặt món, áp dụng khuyến mãi và tìm nhà hàng qua GPS.

## Kiểm thử

```bash
python -m pip install -r requirements.txt
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
coverage run -m unittest discover -s . -p "test_*.py"
coverage report -m
coverage html -d coverage_html
coverage report --fail-under=80
```

Bộ test có 14 ca, gồm 4 ca khuyến mãi và 3 ca GPS theo đề. GPS được thay thế bằng unittest.mock.patch.

## GitHub Actions

Workflow tự chạy khi push hoặc mở pull request vào main, dùng Ubuntu và Python 3.11. Pipeline chạy linter, test, kiểm tra coverage tối thiểu 80% và tải HTML coverage lên artifact trong 7 ngày.

Kết quả local đã kiểm tra trên Windows/Python 3.12.14: 14 test Pass, tổng coverage 98%, yummy_app.py đạt 100%. Xem logs/local_test.log. Kết quả CI thực tế xem trong tab Actions của repository.

Lời giải tham khảo và hướng dẫn minh chứng nằm trong LOI_GIAI_LAB7.md. Bản viết tay, chữ ký và lịch sử thực hành phải được thực hiện thật; repository không giả lập các minh chứng này.
