# -*- coding:utf-8 -*-
'''
    Nếu thứ X(2,3,4,5,6) tạo mức giá cao nhất tuần 
    thì ngày nào trong tuần sẽ thiết lập mức giá ngược lại

    $ python3 Indicator_2.py --symbol=hag --itype=up
    or
    $ python3 Indicator_2.py
''' 

import os
import click
import datetime
import pandas as pd
from pprint import pprint
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from qnaut import Stock, Prices, create_directory


''' ####################
    Lấy & Gom nhóm data
''' ####################
def get_data(symbol, freq, save, offline=False):
    df = None
    # get data online
    if offline == False:
        df = Prices(
            symbol=symbol
            ).get_historical_prices(
                frequency=freq, save=save)
        df.reset_index(inplace = True)
    
    # read data offline
    if offline == True:
        df = pd.read_csv(
            f"./historical_prices/{symbol.upper()}/{freq}_{symbol.upper()}.csv")
    return df

def group_data(df):
    df['Date'] = pd.to_datetime(
        df['Date']
        , format='%Y-%m-%d %H:%M:%S%z')

    df['Week_Number'] = df['Date'].dt.week
    df['Year'] = df['Date'].dt.year
    df['day_of_w'] = df['Date'].dt.dayofweek

    df = df.groupby(['Year', 'Week_Number'])
    return df


''' ##############################
    Đếm các cặp ngày tạo low-high 
''' ##############################
def get_lh_pair(grouped_df):
    low_high_pair = []
    for name, group in grouped_df:
        group = group.drop(columns=['Year', 'Week_Number'])

        low_high_pair.append({
            'week'  : name,
            
            'low'   : group.loc[
                group['Low'] == min(group['Low'])
            ]['day_of_w'].values[0],
            'low_val':min(group['Low']),

            'high'  :group.loc[
                group['High'] == max(group['High'])
            ]['day_of_w'].values[0],
            'high_val':max(group['High'])
        })
    return low_high_pair


''' #######################################################
    Góm nhóm theo ngày bắt đầu và xu hướng tuần: up | down 
''' #######################################################
def go_up_week(low_high_pair, from_day):
    ''' Đếm các tuần go_up
    '''
    def is_go_up(pair_item, from_day):
        if pair_item['high'] >= pair_item['low']:
            if pair_item['low'] == from_day:
                return True
        return False

    go_up = {
        'from_day':from_day,
        'to_day'  :[
            i['high'] 
            for i in low_high_pair 
            if is_go_up(i, from_day)
        ]}
    return go_up

def go_down_week(low_high_pair, from_day):
    ''' Đếm các tuần go_down
    '''
    def is_go_down(pair_item, from_day):
        if pair_item['high'] <= pair_item['low']:
            if pair_item['high'] == from_day:
                return True
        return False

    go_down = {
        'from_day':from_day,
        'to_day'  :[
            i['low'] 
            for i in low_high_pair 
            if is_go_down(i, from_day)
        ]}
    return go_down

def calculate_percent(data):
    def calculate_percent(day, data):
        day_count = len([i for i in data if i==day])
        data_count = len(data)

        if len(data) == 0:
            return 0
        return float("{:.2f}".format(
            100*day_count/data_count
        ))

    percent = [
        calculate_percent(0, data['to_day']),
        calculate_percent(1, data['to_day']),
        calculate_percent(2, data['to_day']),
        calculate_percent(3, data['to_day']),
        calculate_percent(4, data['to_day'])
    ]
    return percent

def indicator_2_up(low_high_pair):
    ''' Go up!
    '''
    up_from_d0 = go_up_week(low_high_pair, 0)
    up_from_d1 = go_up_week(low_high_pair, 1)
    up_from_d2 = go_up_week(low_high_pair, 2)
    up_from_d3 = go_up_week(low_high_pair, 3)
    up_from_d4 = go_up_week(low_high_pair, 4)

    # print(up_from_d0)
    # print(up_from_d1)
    # print(up_from_d2)
    # print(up_from_d3)
    # print(up_from_d4)

    heatdata = [
        calculate_percent(up_from_d0),
        calculate_percent(up_from_d1),
        calculate_percent(up_from_d2),
        calculate_percent(up_from_d3),
        calculate_percent(up_from_d4)
    ]

    return heatdata

def indicator_2_down(low_high_pair):
    ''' GO DOWN
    '''
    down_from_d0 = go_down_week(low_high_pair, 0)
    down_from_d1 = go_down_week(low_high_pair, 1)
    down_from_d2 = go_down_week(low_high_pair, 2)
    down_from_d3 = go_down_week(low_high_pair, 3)
    down_from_d4 = go_down_week(low_high_pair, 4)

    # print(down_from_d0)
    # print(down_from_d1)
    # print(down_from_d2)
    # print(down_from_d3)
    # print(down_from_d4)

    heatdata = [
        calculate_percent(down_from_d0),
        calculate_percent(down_from_d1),
        calculate_percent(down_from_d2),
        calculate_percent(down_from_d3),
        calculate_percent(down_from_d4)
    ]
    return heatdata


@click.command()
@click.option('--symbol', prompt='Symbol? '   , help='Mã CK bạn muốn kiểm tra')
@click.option('--itype' , prompt='itype? (up/down)', help='loại chỉ báo: up hoặc down')

def main(symbol, itype, save_data=True, save_fig=True):
    os.system('cls' if os.name == 'nt' else 'clear')

    # lay & gom nhom data
    df = get_data(symbol, 'daily', save_data, offline=False)
    # df = df.tail(100)
    df = group_data(df)

    # dem cap ngay
    low_high_pair = get_lh_pair(df)
    # pprint(low_high_pair)

    # up
    if itype=='up':
        ax = sns.heatmap(
            data=indicator_2_up(low_high_pair), cmap="YlGnBu"
            , annot=True, cbar=False)

        plt.title("Xác suất thứ X tạo High tuần sau khi thứ Y tạo Low tuần")
        create_directory("./figure")
        if save_fig==True:
            plt.savefig(f"./figure/{symbol.upper()}-up.png")
        plt.show()

    # down
    if itype=='down':
        ax = sns.heatmap(
            data=indicator_2_down(low_high_pair), cmap="YlGnBu"
            , annot=True, cbar=False)

        plt.title("Xác suất thứ X tạo Low tuần sau khi thứ Y tạo High tuần")
        create_directory("./figure")
        if save_fig==True:
            plt.savefig(f"./figure/{symbol.upper()}-down.png")
        plt.show()

if __name__ == "__main__":
    main()