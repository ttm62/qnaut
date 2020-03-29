# -*- coding:utf-8 -*-
'''
    $ python3 Indicator_1.py --help
    or
    $ python3 Indicator_1.py --symbol=HAG --freq=1min --period=120
'''

import os
import sys
import time
import click
from datetime import datetime
from qnaut import Prices, Stock

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def break_high_low(symbol, frequency, force_update=False):
    def break_high(high_col):
        result = []
        length = len(high_col)
        for index in range(0, length):
            if index == 0: 
                result.append(0)
            else:
                if high_col[index] >  high_col[index-1]: result.append(1)
                if high_col[index] <= high_col[index-1]: result.append(0)
        return result

    def break_low(low_col):
        result = []
        length = len(low_col)
        for index in range(0, length):
            if index == 0: 
                result.append(0)
            else:
                if low_col[index] <  low_col[index-1]: result.append(1)
                if low_col[index] >= low_col[index-1]: result.append(0)
        return result

    def break_both(break_high, break_low):
        result = []
        length = len(break_high)
        for index in range(0, length):
            if (break_high[index] == 1 
                and break_low[index] == 1):
                result.append(1)
            else:
                result.append(0)
        return result

    def no_break(break_high, break_low):
        result = []
        length = len(break_high)
        for index in range(0, length):
            if (break_high[index] == 0 
                and break_low[index] == 0):
                result.append(1)
            else:
                result.append(0)
        return result

    def break_vol(break_col, volumn_col):
        result = []
        length = len(break_col)
        for index in range(0, length):
            if break_col[index] == 1:
                result.append(volumn_col[index])
            else:
                result.append(0)
        return result

    df = Prices(
        symbol=symbol
        , force_update=force_update
        ).get_historical_prices(
            frequency=frequency
            , save=True )
    df['break_high']     = break_high(df['High'])
    df['break_high_vol'] = break_vol (df['break_high'], df['Volumn'])
    df['break_low']      = break_low (df['Low'])
    df['break_low_vol']  = break_vol (df['break_low'] , df['Volumn'])    
    df['break_both']     = break_both(df['break_high'], df['break_low'])
    df['no_break']       = no_break  (df['break_high'], df['break_low'])
    df['break_both_vol'] = break_vol (df['break_both'], df['Volumn'])
    df['no_break_vol']   = break_vol (df['no_break']  , df['Volumn'])

    return df


def stat_in_percent(col):
    return "{:.2f}".format(
        100*sum(col)/len(col))

def terminal_stat(df):
    stat    = {}
    df      = df.reset_index()

    stat['break_high'] = {
        'count'     : sum(df['break_high']) 
        , 'percent' : stat_in_percent(df['break_high'])
        , 'volumn'  : sum(df['break_high_vol'])
    }

    stat['break_low'] = {
        'count'     : sum(df['break_low']) 
        , 'percent' : stat_in_percent(df['break_low'])
        , 'volumn'  : sum(df['break_low_vol'])
    }

    stat['break_both'] = {
        'count'     : sum(df['break_both']) 
        , 'percent' : stat_in_percent(df['break_both'])
        , 'volumn'  : sum(df['break_both_vol'])
    }

    stat['no_break'] = {
        'count'     : sum(df['no_break']) 
        , 'percent' : stat_in_percent(df['no_break'])
        , 'volumn'  : sum(df['no_break_vol'])
    }

    stat['start'] = df['Date'][0].ctime()
    stat['end']  = df['Date'][len(df['Date'])-1].ctime()

    sum_vol = 0
    sum_vol += stat['break_high']['volumn']
    sum_vol += stat['break_low']['volumn']
    sum_vol += stat['break_both']['volumn']
    sum_vol += stat['no_break']['volumn']

    def vol_percent(vol, sum_vol):
        return "{:.2f}".format(
            100*vol/sum_vol)

    def line_stat(name, color, stat_dict):
        print(
            f"{color}{name}: {stat_dict['percent']}% \t\b\b\b({stat_dict['count']})\t\b\b\bvol:{vol_percent(stat_dict['volumn'],sum_vol)}%{bcolors.ENDC}")

    print(f"[From]: \t{stat['start']}\n[To]: \t\t{stat['end']}")
    print()
    line_stat("Break high", bcolors.OKGREEN, stat['break_high'])
    line_stat("Break  low", bcolors.FAIL   , stat['break_low'] )
    line_stat("Break both", bcolors.HEADER , stat['break_both'])
    line_stat("No   break", bcolors.WARNING, stat['no_break']  )
    print()

@click.command()
@click.option('--symbol', prompt='Symbol? '   , help='Mã CK bạn muốn kiểm tra')
@click.option('--freq'  , prompt='frequency? ', help='Khung thời gian (1min, 5min, 10min, ... daily, monthly, weekly)')
@click.option('--period', default=120         , help='Thời gian tự động làm mới kết quả (s)')

def main(symbol, freq, period):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("="*40)
        print(f"= ({Stock(symbol).get_symbol()}-{freq}) Xac suat pha vo High\Low")
        print("="*40)
        df = break_high_low(
            symbol=symbol, frequency=freq)
        terminal_stat(df)
        
        print(f"[Last update]\n{datetime.now().ctime()}")
        time.sleep(period)

if __name__ == "__main__":
    main()