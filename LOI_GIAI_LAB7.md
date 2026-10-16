# Bài thực hành 7 - YummyApp Mocking và CI/CD

Đây là bài giải mã nguồn và tài liệu tham khảo để thực hiện bài. Các trang viết tay, chữ ký, lịch sử commit cá nhân và bằng chứng GitHub Actions cần được tạo từ quá trình làm thật. Chưa có họ tên, MSSV, email và URL repository nên không điền giả các thông tin này.

## 1. Sơ đồ để vẽ tay (trang 1)

Git Push Event → Checkout Code → Setup Python 3.11 → Install Dependencies → Execute Unit Tests → Quality Gate.

Quality Gate: coverage ≥ 80% thì Pass, dưới 80% thì Fail. Trong workflow hoàn chỉnh, chèn Static Code Analysis trước Execute Unit Tests; sau Quality Gate là bước upload HTML artifact. Lỗi linter làm các bước test bị bỏ qua. Bước upload có `if: always()` nên vẫn được thử chạy; nếu linter thất bại trước khi sinh HTML thì không có báo cáo để tải lên.

Mỗi trang viết tay ghi họ tên, MSSV, ngày thực hành và ký bằng bút mực xanh theo đề.

## 2. Ma trận 7 ca Mocking bắt buộc (trang 2)

| Tên test case | Hàm được gọi | Đối tượng & giá trị Mocking | Kết quả kỳ vọng (Assert) |
|---|---|---|---|
| Online hợp lệ | apply_promo_code(100000, "GIAM10") | YummyApp(network_status="online", os_version=15) | assertAlmostEqual(kết quả, 90000) |
| Offline | apply_promo_code(100000, "GIAM10") | YummyApp(network_status="offline") | assertRaises(ConnectionError) |
| Mã đặc biệt OS 15 | apply_promo_code(100000, "NEW_OS_ONLY") | YummyApp(os_version=15) | assertAlmostEqual(kết quả, 80000) |
| Mã đặc biệt OS 14 | apply_promo_code(100000, "NEW_OS_ONLY") | YummyApp(os_version=14) | assertRaises(ValueError) |
| GPS trong vùng | get_nearby_restaurants() | patch yummy_app.gps_service.get_current_location; return_value=(10.0, 105.0) | Bằng ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"] |
| GPS ngoài vùng | get_nearby_restaurants() | Cùng patch; return_value=(20.0, 110.0) | Bằng [] |
| GPS mất tín hiệu | get_nearby_restaurants() | Cùng patch; side_effect=GPSSignalLostError | Bằng "Khong the xac dinh vi tri." |

Bốn ca khuyến mãi giả lập môi trường bằng trạng thái constructor vì mã khởi tạo không gọi API mạng thật. Offline làm chính hàm nghiệp vụ ném ConnectionError; không patch hàm đang cần kiểm thử. Ba ca GPS dùng đúng đường dẫn patch tại nơi hàm được sử dụng, đồng thời kiểm tra mock được gọi đúng một lần và không truyền đối số.

Bộ test có thêm mã khuyến mãi không tồn tại, món không có trong menu và số lượng âm để kiểm tra các nhánh còn thiếu. Giữ nguyên MENU và nghiệp vụ do đề cung cấp.

## 3. Trả lời Cấp độ 2 (trang 3)

### Câu 2.1

Linter cần chạy trước test để phát hiện sớm lỗi cú pháp và một số lỗi tĩnh như tên biến chưa định nghĩa. Nếu mã không thể phân tích hoặc import thì chạy test tiếp thường chỉ tạo thêm lỗi dây chuyền, tốn tài nguyên và làm khó xác định nguyên nhân. Nguyên tắc fail-fast giúp trả phản hồi sớm cho người phát triển. Linter không thay thế unit test: linter kiểm tra cấu trúc mã, unit test kiểm tra hành vi và kết quả nghiệp vụ. Bộ chọn E9,F63,F7,F82 trong đề chỉ bật nhóm lỗi được chỉ định, không phải toàn bộ quy tắc phong cách flake8.

### Câu 2.2

`coverage report --fail-under=80` so sánh độ bao phủ tổng hợp với ngưỡng 80%. Nếu không đạt, coverage trả mã thoát 2; khi thành công bình thường trả 0. Shell và GitHub Actions sử dụng mã thoát để biết lệnh thành công hay thất bại. Với cấu hình run mặc định trên Ubuntu, lệnh thất bại khiến step và job thất bại; các step sau theo điều kiện thành công mặc định sẽ bị bỏ qua. Step có `if: always()` vẫn được xem xét chạy. Linux không tự hiểu khái niệm coverage: chương trình coverage quyết định mã thoát, runner dùng mã đó để đánh dấu kết quả. Không sử dụng continue-on-error hay `|| true` cho Quality Gate vì sẽ che lỗi.

Lưu ý: workflow thất bại chỉ ngăn merge khi repository đã bật quy tắc bảo vệ nhánh yêu cầu status check này phải thành công.

### Câu 2.3

Tham số `-m` (show missing) bổ sung cột Missing, chỉ rõ số dòng hoặc khoảng dòng chưa được thực thi, ví dụ `24-25, 31`. Kỹ sư đọc các dòng đó, xác định điều kiện dẫn tới nhánh chưa chạy và thêm test có dữ liệu/mock phù hợp. Nhờ vậy có thể bổ sung kiểm thử có mục tiêu thay vì chỉ nhìn phần trăm tổng. Dòng đã được chạy chưa chứng minh assert đủ mạnh; vẫn phải kiểm tra kết quả và ngoại lệ. Coverage theo nhánh cần bật riêng bằng `--branch`; lệnh trong đề mặc định đo theo dòng.

## 4. Trả lời Cấp độ 3 (trang 4)

### Câu 3.1

Flaky Test là test có lúc Pass, lúc Fail dù không thay đổi mã và điều kiện đầu vào chủ đích. Nguyên nhân thường là phụ thuộc thời gian, thứ tự chạy, trạng thái dùng chung, bất đồng bộ hoặc dịch vụ bên ngoài không ổn định. Ví dụ test gọi GPS thật có thể Pass khi nhận đúng tọa độ nhưng Fail khi thiết bị mất tín hiệu. Dùng patch với return_value hoặc side_effect giúp kiểm soát điều kiện và tái lập kết quả.

Lỗi sai lệch môi trường phụ thuộc xảy ra khi máy cá nhân và CI dùng khác Python, thư viện hoặc cấu hình; chẳng hạn API thay đổi trong phiên bản thư viện mới khiến CI luôn Fail còn local luôn Pass. Lỗi này thường tái lập được khi tái tạo đúng môi trường bị lỗi. Cần so sánh phiên bản, cấu hình và log; ghim dependencies, thống nhất Python và dùng môi trường sạch. Hai nhóm nguyên nhân có thể cùng xuất hiện nên cần kiểm chứng thay vì suy đoán chỉ từ một lần Fail.

### Câu 3.2

Ghim phiên bản trực tiếp bằng `==` giúp local và CI cài cùng phiên bản đã kiểm tra, tránh tự động nhận bản mới làm thay đổi API hoặc hành vi và giúp điều tra, tái hiện, rollback. Theo đề: requests==2.31.0, coverage==7.4.0, flake8==7.0.0. Tuy nhiên chỉ ghim ba thư viện trực tiếp chưa khóa toàn bộ môi trường: phụ thuộc bắc cầu, bản vá Python và runner vẫn có thể đổi. Dự án cần tái lập chặt hơn nên quản lý thêm lock/constraints và môi trường chạy. Pinning không có nghĩa giữ phiên bản cũ mãi; vẫn phải chủ động đánh giá, thử nghiệm và cập nhật.

### Câu 3.3 - Sáu bước nâng cấp an toàn

1. Đồng bộ main đang xanh; tạo nhánh riêng như `chore/update-requests` để không sửa trực tiếp main.
2. Đọc changelog, thay đổi phá vỡ tương thích, yêu cầu Python và vấn đề bảo mật; xác định phiên bản đích cụ thể và phạm vi ảnh hưởng.
3. Sửa phiên bản ghim trong requirements.txt (và lock/constraints nếu có); cài lại trong môi trường sạch, sửa mã tương thích nếu cần.
4. Chạy linter, unit test, các test tích hợp liên quan và coverage; bảo đảm đạt Quality Gate, bổ sung test có ý nghĩa cho hành vi thay đổi.
5. Commit, push nhánh và mở Pull Request vào main; mô tả phiên bản cũ/mới, thay đổi, bằng chứng test và cách rollback. Đợi CI trên PR thành công và review được chấp thuận.
6. Merge khi các check bắt buộc đã đạt; theo dõi CI trên main và hành vi sau cập nhật. Nếu lỗi, revert commit/PR nâng cấp về phiên bản trước rồi điều tra trên nhánh riêng.

## 5. Chạy trên máy

Chạy trong thư mục dự án với Python 3.11 theo đề. Môi trường kiểm tra có thể xem trong logs/local_test.log; không coi môi trường Windows local là Ubuntu GitHub Actions.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
.\.venv\Scripts\python.exe -m coverage run -m unittest discover -s . -p "test_*.py" > logs/local_test.log 2>&1
.\.venv\Scripts\python.exe -m coverage report -m >> logs/local_test.log
.\.venv\Scripts\python.exe -m coverage html -d coverage_html
.\.venv\Scripts\python.exe -m coverage report --fail-under=80
```

## 6. Tạo minh chứng GitHub đúng trình tự

Không commit ngay bộ test cuối nếu cần chứng minh toàn bộ quá trình Đỏ → Xanh. Lưu bản cuối ở ngoài repository trước, rồi thực hiện từng giai đoạn sau trên repo của bạn.

1. Khởi tạo Git, đặt tên tác giả bằng MSSV và họ tên thật, đặt email thật. Bản đầu chỉ giữ bốn test mẫu của TestEasyLevel; tạo workflow cơ bản bốn bước theo trang 3 (bước 4 chạy `python -m unittest discover -s . -p "test_*.py"`). Commit và push lên main, chụp lần CI cơ bản Pass.
2. Thêm linter và Quality Gate như file workflow cuối. Giữ bộ test mẫu, commit và push để có lần CI Fail vì coverage dưới 80%. Con số khoảng 35% trong đề là ước lượng; dùng số đo thực tế, không sửa log cho khớp.
3. Hoàn thành bảng viết tay trước khi bổ sung test. Khôi phục bộ test cuối, commit và push; chụp lần CI Pass và coverage ≥85%.
4. Break the Build: thêm tạm `def broken_function(` vào yummy_app.py, commit và push. Chụp lần Fail ở linter; xác nhận bước test bị bỏ qua. Sau đó xóa dòng lỗi, commit và push; chụp lần phục hồi Pass. Không giữ lỗi trong bản nộp cuối.
5. Thêm bước upload artifact nếu chưa có; push bản cuối và tải YummyApp-Coverage-Report từ run thành công. Thu raw log của run cuối vào logs/github_actions_run.log. Nếu tải archive chứa nhiều log, giữ archive gốc ngoài hoặc trong evidence và ghép nguyên văn các log step theo thứ tự; không tự viết nội dung như thể đã chạy trên GitHub.
6. Xuất lịch sử bằng lệnh bên dưới sau các commit minh chứng. Sau khi commit thêm tài liệu/log, xuất lại git_history.log để phản ánh lịch sử mới nhất trước khi đóng gói.

```powershell
git init -b main
git config user.name "MSSV - Ho Va Ten"
git config user.email "mssv@dlu.edu.vn"
git add .
git commit -m "Khoi tao YummyApp va CI co ban"
git remote add origin https://github.com/TAI_KHOAN/REPOSITORY.git
git push -u origin main
git log --graph --pretty=format:"%h - %an (%ad): %s" > logs/git_history.log
```

Thay các giá trị tài khoản và định danh bằng thông tin thật trước khi chạy. Những lệnh commit/push tiếp theo thực hiện theo từng giai đoạn ở trên. Chưa tạo lịch sử Git hoặc raw log GitHub trong bài mẫu này vì chưa có định danh và repository của bạn.

## 7. Hoàn thiện báo cáo và đóng gói

Đổi thư mục gốc thành `MSSV_HoTen_Lab7`. Bản nộp bắt buộc có .github/workflows/yummyapp-ci.yml, ba file Python, requirements.txt, ba log thật, MinhChung_VietTay_MSSV.pdf và BaoCao_KetQua_Lab7.pdf.

MinhChung_VietTay_MSSV.pdf gồm bốn trang tự viết: sơ đồ; bảng bảy ca; câu 2.1-2.3; câu 3.1-3.3. Ghi định danh, ngày làm và chữ ký trên từng trang. Tài liệu gõ máy này là tham khảo, không thay thế bản scan viết tay.

BaoCao_KetQua_Lab7.pdf cần có: họ tên/MSSV/lớp/ngày; link GitHub công khai và nhánh; mô tả môi trường, số test và coverage thực đo; ảnh và URL run cho CI cơ bản Pass, coverage Fail, sau bổ sung test Pass, linter Fail và phục hồi Pass; ảnh artifact và nhận xét; kết luận đối chiếu mục tiêu. Không dùng ảnh/log local thay cho bằng chứng run GitHub.

Kiểm tra đủ bằng chứng rồi nén thư mục thành `MSSV_HoTen_Lab7.zip`. Không cần đưa .venv, __pycache__ hoặc khóa/thông tin đăng nhập vào ZIP.
