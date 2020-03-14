### (rất xin lỗi các bạn vì hiện tại chưa có document để sử dụng, mình sẽ làm nó sớm)
### Xem các ví dụ trong file example.py

```python
# để bắt đầu, nhập module này vào chương trình của bạn
from qnaut import *

# khởi tạo đối tượng với mã CK bạn cần, ở đây là 'FPT'
fpt = prices(symbol='FPT')

# thông tin về công ty
print(
    fpt.get_company_info())

# ====== Kết quả (JSON)
# {'object': 'stock', 'id': '829', 'symbol': 'FPT', 'company': 'Công ty Cổ phần FPT'
# , 'companyName': 'Công ty Cổ phần FPT', 'companyNameEng': 'FPT Corporation'
# , 'shortName': 'CTCP FPT', 'status': 'listed', 'listedDate': '2006-12-13'
# , 'delistedDate': None, 'floor': 'HOSE', 'indexCode': 'VN30', 'industryName': 'Dịch vụ máy tính'}

# sự kiện
print(
    fpt.get_events())

# ====== Kết quả (JSON)
# {'object': 'list', 'totalCount': 80, 'data': [{'id': '32280', 'symbol': 'FPT', 'group': 'investorRight'
# , 'type': 'MEETING', 'typeDesc': 'Họp cổ đông', 'effectiveDate': '2019-02-28', 'disclosuredDate': '2019-01-30'
# , 'expiredDate': '2019-03-29', 'content': 'ĐHĐCĐ thường niên năm 2019 \n', 'actualDate': '2019-03-29'
# , 'object': 'events'}, {'id': '30495', 'symbol': 'FPT', 'group': 'investorRight', 'type': 'DIVIDEND'
# , 'typeDesc': 'Cổ tức bằng tiền', 'effectiveDate': '2018-08-16', 'disclosuredDate': '2018-08-01'
# , 'expiredDate': '2018-08-31', 'content': 'Tạm ứng cổ tức đợt 1/2018 (1000 đ/cp)', 'dividend': 1000
# , 'ratio': 10.0, 'actualDate': '2018-08-31', 'divPeriod': 1, 'divYear': 2018, 'object': 'events'}, .......}

# lịch sử giá (CSV) 
print(
    fpt.get_historical_prices(
        start='2018'
        , end='2019'
        , frequency="monthly"
        , save=False))

# ====== Kết quả (CSV)
# hỗ trợ gần như tất cả các khung thời gian:
# monthly, weekly, daily, 60min, 30min, 15min, 10min, 5min, 3min

# mặc định kết quả dạng CSV sẽ lưu ở thư mục cùng tên với mã bạn đang tìm trong thư mục historical_prices,
# và sẽ không lưu nếu save=False

# kiểu khác

# print(
#     fpt.get_historical_prices(
#         start='2018-01-02'
#         , end='2018-01-05'
#         , frequency="5min"))

# print(
#     fpt.get_historical_prices(
#         start='2018-11'
#         , end='2019-01'
#         , frequency="weekly"
#         , save=False))

# print(
#     fpt.get_historical_prices(
#         start='2019-01-02 09:15:00+07:00'
#         , end='2019-01-04 18:00:00+07:00'
#         , frequency="5min"))

```
