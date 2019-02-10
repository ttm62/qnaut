import os
import json
import datetime
import requests as rq
import pandas as pd

from logger import log

# thong so thoi gian mac dinh (Unix timestamp)
start_default = pd.Timestamp('2016-01-01').value // (10**9)
end_default = pd.Timestamp(datetime.datetime.now().date()).value // (10**9)

def check_dir(dir_name):
    '''Tao thu muc neu chua ton tai
    '''
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        log(
            'info'
            , 'Directory {dir_name} created'
            .format(dir_name=dir_name))

def write_to_json(folder, fileName, data):
    '''ghi ra file json
    '''
    filePathNameWExt = None
    try:
        filePathNameWExt = './' + folder + '/' + fileName + '.json'
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)
    except:
        log(
            'warning'
            ,'Loi ghi file {file} tu write_to_json()'
            .format(file=filePathNameWExt))

def update_data():
    '''cap nhat du lieu thi truong va luu cuc bo
    '''
    try:
        # tat ca ma niem yet CP tren cac san
        r = rq.get(
            'https://finfo-api.vndirect.com.vn/stocks'
        ).json()
        write_to_json('info', 'vn_by_symbol', r)

        # ma CP theo nganh
        r = rq.get(
            'https://finfo-api.vndirect.com.vn/industries'
        ).json()
        write_to_json('info', 'vn_by_industries', r)

        log('info', 'Da cap nhat du lieu thi truong viet nam update_data()')
        return True
    except:
        log(
            'warning'
            ,'Loi cap nhat du lieu tu update_data()')
        return False

class prices():
    def __init__(self,symbol):
        '''Chuan bi du lieu theo symbol
        '''
        # kiem tra duong dan co ban
        check_dir('./info')
        check_dir('./events')
        check_dir('./historical_prices')

        # khoi tao bien cho moi instance
        self.symbol = symbol.upper()
        self.company_info = None
        self.events = None
        self.historical_prices = None
        
        # kiem tra du lieu da co san hay chua? -> cap nhat
        if not os.path.exists('./info/vn_by_symbol.json') and not os.path.exists('./info/vn_by_industries.json'):
            update_data()
        
        # tim du lieu tuong ung voi symbol va cap nhat events
        with open('./info/vn_by_symbol.json') as f:
            r = json.load(f)
            f.close()
            for i in r['data']:
                # neu co thong tin ve ma CP 
                if i['symbol'] in [self.symbol]:
                    self.company_info = i
                    try:
                        r = rq.get(
                            'https://finfo-api.vndirect.com.vn/events?symbols={symbol}'
                            .format(symbol=self.symbol)).json()
                        self.events = r if r else None
                        write_to_json(
                            'events'
                            , '{symbol}_events'
                            .format(symbol=self.symbol)
                            , r)
                        log(
                            'info'
                            , 'Da yeu cau ma CP: {symbol}'
                            .format(symbol=self.symbol))
                    except:
                        log(
                            'warning'
                            , 'Da yeu cau ma CP: {symbol}'
                            .format(symbol=self.symbol))

    def get_company_info(self):
        return self.company_info

    def get_events(self):
        return self.events
    
    def get_historical_prices(self, start=start_default
        , end=end_default, frequency="daily", save=True):
        def save_to_csv(df, symbol, frequency):
            # chuan bi thu muc de luu du lieu lich su gia 
            check_dir(
                './historical_prices/{symbol}'
                .format(symbol=self.symbol))
            # luu lai
            df.to_csv(
                './historical_prices/{symbol_upper}/{frequency}_{symbol}.csv'
                .format(
                    frequency=frequency
                    ,symbol_upper=symbol.upper() 
                    ,symbol=symbol))

        def api_builder(symbol, frequency, start=start_default, end=end_default):
            if frequency.lower() in ["daily", "weekly", "monthly", "d", "w", "m"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='D'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["60min", "60"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='60'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["30min", "30"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='30'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["15min", "15"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='15'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["10min", "10"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='10'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["5min", "5"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='5'
                    , start_date = start
                    , end_date = end)
            elif frequency.lower() in ["3min", "3"]:
                return 'https://api.vietstock.vn/ta/history?symbol={symbol}&resolution={frequency}&from={start_date}&to={end_date}'.format(
                    symbol=symbol
                    , frequency='3'
                    , start_date = start
                    , end_date = end)
        
        # ================== CHECKPOINT =====================
        # print(self.symbol, frequency, start, end)
        # print(api_builder(
        #         symbol=self.symbol
        #         ,frequency=frequency
        #         ,start=pd.Timestamp(start).value // (10**9)
        #         ,end=pd.Timestamp(end).value // (10**9)))
        # ===================================================

        # Lay du lieu tu API vietstock
        r = rq.get(
            api_builder(
                symbol=self.symbol
                ,frequency=frequency
                ,start=pd.Timestamp(start).value // (10**9)
                ,end=pd.Timestamp(end).value // (10**9))
            ).json()

        df = pd.read_json(r)
        # rename cac cot
        df.rename(
            index=str
            , columns={
                't': 'Date'
                ,'o': 'Open'
                ,'h': 'High'
                ,'l': 'Low'
                ,'c': 'Close'
                ,'v': 'Volumn'}
            , inplace=True)
        # xoa cot s
        df.drop("s", axis=1, inplace=True)
        # lam tron 2 chu so thap phan
        df = df.round({
            'Close': 2
            ,'Open': 2
            ,'High': 2
            ,'Low': 2})
        # chuan hoa datetime cho cot Date
        df['Date'] = pd.to_datetime(df['Date'], unit='s')
        # chuyen doi timezone thanh Asia/Ho_Chi_Minh (pytz)
        df.Date = df.Date.dt.tz_localize('UTC').dt.tz_convert('Asia/Ho_Chi_Minh')

        # neu frequency la "monthly" hoac "weekly" thi
        if frequency.lower() in ["weekly", "w"]:
            df['Week_Number'] = df['Date'].dt.week
            df['Year'] = df['Date'].dt.year
            df = df.groupby(['Year','Week_Number']).agg({
                'Date':'first'
                ,'Open':'first'
                , 'High':'max'
                , 'Low':'min'
                , 'Close':'last'
                , 'Volumn':'sum'})
            # # chuyen index thanh cot Date
            # df.set_index('Date', inplace=True)
        elif frequency.lower() in ["monthly", "m"]:
            df['Month_Number'] = df['Date'].dt.month
            df['Year'] = df['Date'].dt.year
            df = df.groupby(['Year','Month_Number']).agg({
                'Date':'first'
                ,'Open':'first'
                , 'High':'max'
                , 'Low':'min'
                , 'Close':'last'
                , 'Volumn':'sum'})
            # # chuyen index thanh cot Date
            # df.set_index('Date', inplace=True)
        
        # chuyen index thanh cot Date
        df.set_index('Date', inplace=True)
        # luu csv
        if save is True:
            save_to_csv(df, self.symbol, frequency=frequency)
        return df
