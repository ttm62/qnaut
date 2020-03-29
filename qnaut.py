# -*- coding:utf-8 -*-
__all__ = ['Stock','Prices','create_directory']   # ngăn chặn wild import

import os
import json
import datetime
import requests as rq
import pandas as pd

from logger import log

DEFAULT_TIMEDELTA = 7

#####################
#       HELPER
#####################

def create_directory(directory):
    ''' Tạo thư mục nếu chưa tồn tại
    '''
    exist_dir = os.path.exists(directory)
    if not exist_dir:
        os.mkdir(directory)


def write_json(data, folder, fileName):
    ''' Ghi json ra file
    '''
    filePathNameWithExt = None
    try:
        filePathNameWithExt = './' + folder + '/' + fileName + '.json'
        with open(filePathNameWithExt, 'w') as fp:
            json.dump(data, fp)
    except:
        log("warning", f"Loi ghi file {filePathNameWithExt} tu write_json()")


def update_data(last_update, force):
    ''' Cập nhật dữ liệu và lưu cục bộ
        (tự động cập nhật nếu last_update là 3 ngày trước)
    '''
    this_moment = datetime.datetime.now()
    if this_moment-last_update >= datetime.timedelta(days=DEFAULT_TIMEDELTA):
        try:
            # tat ca cac ma CP dang niem yet
            data = rq.get("https://finfo-api.vndirect.com.vn/stocks").json()
            write_json(data, 'info', 'vn_by_symbol')

            # data phan chia theo nganh
            data = rq.get(
                "https://finfo-api.vndirect.com.vn/industries"
            ).json()
            write_json(data, "info", "vn_by_industries")

            log("info", "Da cap nhat du lieu thi truong Viet Nam")
        except:
            log("warning", "Loi cap nhat du lieu tu update_data()")

    if force == True:
        try:
            # tat ca cac ma CP dang niem yet
            data = rq.get("https://finfo-api.vndirect.com.vn/stocks").json()
            write_json(data, 'info', 'vn_by_symbol')

            # data phan chia theo nganh
            data = rq.get(
                "https://finfo-api.vndirect.com.vn/industries"
            ).json()
            write_json(data, "info", "vn_by_industries")

            log("info", "Da cap nhat du lieu thi truong Viet Nam")
        except:
            log("warning", "Loi cap nhat du lieu tu update_data()")
    return this_moment


def api_builder(symbol, frequency, start, end):
    if frequency.lower() in ["daily", "weekly", "monthly", "d", "w", "m"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=D&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=D&symbol={symbol}"
    elif frequency.lower() in ["60min", "60"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=60&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=60&symbol={symbol}"
    elif frequency.lower() in ["30min", "30"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=30&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=30&symbol={symbol}"
    elif frequency.lower() in ["15min", "15"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=15&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=15&symbol={symbol}"
    elif frequency.lower() in ["10min", "10"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=10&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=10&symbol={symbol}"
    elif frequency.lower() in ["5min", "5"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=5&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=5&symbol={symbol}"
    elif frequency.lower() in ["1min", "1"]:
        if start and end:
            return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=1&symbol={symbol}&from={start}&to={end}"
        return f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=1&symbol={symbol}"


def save_to_csv(df, symbol, frequency):
    # chuan bi thu muc de luu du lieu lich su gia 
    create_directory(f"./historical_prices/{symbol.upper()}")
    # luu lai
    df.to_csv(
        f"./historical_prices/{symbol.upper()}/{frequency}_{symbol}.csv")


#####################
#     MAIN PART
#####################

class Stock():
    last_update = datetime.datetime.now()

    def __init__(self, symbol, force_update=False):
        # kiem tra duong dan co ban
        create_directory("./info")
        create_directory("./events")
        create_directory("./historical_prices")

        # khoi tao bien
        self.symbol       = symbol.upper()
        self.company_info = None
        self.events       = None
        self.force_update = force_update

        # cap nhat data
        Stock.last_update = update_data(Stock.last_update, self.force_update)

    def is_exists(self):
        # kiem tra du lieu da co san hay chua? -> cap nhat
        if (not os.path.exists("./info/vn_by_symbol.json") and
            not os.path.exists("./info/vn_by_industries.json")):
            Stock.last_update = update_data(Stock.last_update, self.force_update)

        # tim du lieu tuong ung voi symbol va cap nhat events
        with open("./info/vn_by_symbol.json") as f:
            data = json.load(f)
            for i in data["data"]:
                # neu co thong tin ve ma CP
                if i["symbol"] in [self.symbol]:
                    self.company_info = i
                    return True
        return False
    
    def get_symbol(self):
        return self.symbol.upper()

    def get_info(self):
        if self.company_info is not None:
            return self.company_info
        else:
            with open("./info/vn_by_symbol.json") as f:
                data = json.load(f)
                for i in data["data"]:
                    # neu co thong tin ve ma CP
                    if i["symbol"] in [self.symbol]:
                        self.company_info = i
        return self.company_info

    def get_events(self):
        data = rq.get(
            f"https://finfo-api.vndirect.com.vn/events?symbols={self.symbol}"
        ).json()

        self.events = data if data else None
        write_json(data, "events", f"{self.symbol}_events")
        return self.events


class Prices():
    def __init__(self, symbol, force_update=False):
        self.company            = Stock(symbol=symbol, force_update=force_update)
        self.historical_prices  = None
    
    def get_company(self):
        return self.company

    def get_historical_prices(self, frequency, start=None, end=None, save=True):
        if not self.company.is_exists():
            return None
        else:
            # Lay du lieu tu API vndirect
            df = pd.read_json(
                api_builder(
                    symbol      = self.company.get_symbol()
                    ,frequency  = frequency
                    ,start      = pd.Timestamp(start).value // (10**9) if start else None
                    ,end        = pd.Timestamp(end  ).value // (10**9) if end   else None
                ))
            
            # rename cac cot
            df.rename(
                index=str
                , columns={
                't': 'Date'
                ,'o': 'Open' ,'h': 'High'
                ,'l': 'Low'  ,'c': 'Close'
                ,'v': 'Volumn'}
            , inplace=True)

            # xoa cot s
            df.drop("s", axis=1, inplace=True)
            # lam tron 2 chu so thap phan
            df = df.round({
                'Close': 2 ,'Open': 2
                ,'High': 2 ,'Low': 2 })
            # chuan hoa datetime cho cot Date
            df['Date'] = pd.to_datetime(df['Date'], unit='s')
            # chuyen doi timezone thanh Asia/Ho_Chi_Minh (pytz)
            df.Date = df.Date.dt.tz_localize('UTC').dt.tz_convert('Asia/Ho_Chi_Minh')

            '''
                neu frequency la "monthly" hoac "weekly" thi gom nhom data
            '''
            if frequency.lower() in ["weekly", "w"]:
                df['Week_Number'] = df['Date'].dt.week
                df['Year'] = df['Date'].dt.year
                df = df.groupby(['Year','Week_Number']).agg({
                    'Date':'first'
                    ,'Open':'first' , 'Close':'last'
                    , 'High':'max'  , 'Low':'min'
                    , 'Volumn':'sum' })

            elif frequency.lower() in ["monthly", "m"]:
                df['Month_Number'] = df['Date'].dt.month
                df['Year'] = df['Date'].dt.year
                df = df.groupby(['Year','Month_Number']).agg({
                    'Date':'first'
                    ,'Open':'first', 'Close':'last'
                    , 'High':'max' , 'Low':'min'
                    , 'Volumn':'sum' })

            # chuyen index thanh cot Date
            df.set_index('Date', inplace=True)
            # luu csv
            if save is True:
                save_to_csv(
                    df, self.company.get_symbol(), frequency=frequency )
            return df

