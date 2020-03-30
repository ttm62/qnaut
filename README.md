### Cai dat cac phu thuoc
$ pip install pandas numpy seaborn matplotlib click 

### Su dung
```python
# -*- coding:utf-8 -*-
from pprint import pprint

# để bắt đầu, nhập module này vào chương trình của bạn
from qnaut import *

#####################
#   TÌM THÔNG TIN
#####################

# khởi tạo đối tượng với mã CK bạn cần, ở đây là 'HAG'
test1 = Stock(symbol="hag")

pprint(test1.is_exists())        # kiểm tra xem mã có tồn tại không
''' =====>
    True
'''

pprint(test1.get_info())         # xem thông tin cơ bản
''' =====>
{'company': 'Công ty Cổ phần Hoàng Anh Gia Lai',
 'companyName': 'Công ty Cổ phần Hoàng Anh Gia Lai',
 'companyNameEng': 'HAGL Joint Stock Company',
 'delistedDate': None,
 'floor': 'HOSE',
 'id': '2374',
 'indexCode': None,
 'industryName': 'Đầu tư và phát triển bất động sản',
 'listedDate': '2008-12-22',
 'object': 'stock',
 'shortName': 'Hoàng Anh Gia Lai',
 'status': 'listed',
 'symbol': 'HAG'}
'''

pprint(test1.get_events())       # xem các sự kiện 
''' =====>
{'data': [{'content': 'Chậm CBTT Nghị quyết HĐQT',
           'disclosuredDate': '2019-11-05',
           'effectiveDate': '2019-11-04',
           'group': 'stockAlert',
           'id': 'HAGAAAZ+TAALAAE/YeAAJ',
           'locale': 'VN',
           'object': 'events',
           'symbol': 'HAG',
           'type': 'noticed',
           'typeDesc': 'Nhắc nhở'},
           ........
'''

###################
#   LỊCH SỬ GIÁ
#   hỗ trợ gần tất cả các khung thời gian:
#   monthly, weekly, daily, 60min, 30min, 15min, 10min, 5min, 1min
###################
test2 = Prices(symbol="hag")

print(
    test2.get_historical_prices(
        frequency="monthly"
        , save=False))

''' =====>
                           Open  Close   High   Low     Volumn
Date                                                          
2016-03-28 07:00:00+07:00  8.20   7.80   8.30  7.70   14865310
2016-04-01 07:00:00+07:00  7.80   8.00   8.10  6.50   91000860
2016-05-04 07:00:00+07:00  7.90   7.80   8.90  7.20   52933030
2016-06-01 07:00:00+07:00  7.80   7.30   8.20  7.00   68080750
2016-07-01 07:00:00+07:00  7.30   6.40   7.50  6.30   50947890
2016-08-01 07:00:00+07:00  6.50   6.30   7.10  5.00  116386220
2016-09-01 07:00:00+07:00  6.20   5.25   6.20  4.93   64217000
2016-10-03 07:00:00+07:00  5.25   5.20   5.95  5.02   49393050
    ........
'''

#############################################
#   Một số cách dùng khác
#   lưu ý có giới hạn lấy dữ liệu nên 
#   nếu thấy trả về dataframe rỗng thì
#   b cần chỉnh lại thời gian và frequency 
#############################################

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
#     test3.get_historical_prices(
#         start='2019-01-02 09:15:00+07:00'
#         , end='2019-01-12 18:00:00+07:00'
#         , frequency="daily" ))
```
