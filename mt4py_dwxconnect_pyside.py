# add logging to each function in the code
# https://stackoverflow.com/questions/13733552/python-logging-function-name-and-line-number-for-each-call


import json
from time import sleep
from threading import Thread
from os.path import join, exists
from traceback import print_exc
from random import random
from datetime import datetime, timedelta

from api.dwx_client import dwx_client
import xlwings as xw
import time



"""

Example dwxconnect client in python


This example client will subscribe to tick data and bar data. It will also request historic data. 

!!! ----- IMPORTANT ----- !!!

If open_test_trades=True, it will open many trades. 
Please only run this on a demo account!

!!! ----- IMPORTANT ----- !!!

"""

file_path = 'C:\\Users\\Kalyan\\Downloads\\pyxl_testbook.xlsx'

class tick_processor():
    def __init__(self, MT4_directory_path, sleep_delay=0.005,  # 5 ms for time.sleep()
            max_retry_command_seconds=10,  # retry to send the commend for 10 seconds if not successful.
            verbose=True):
        # if true, it will randomly try to open and close orders every few seconds.
        self.open_test_trades = False
        self.last_open_time = datetime.utcnow()
        self.last_modification_time = datetime.utcnow()
        self.index_column_arr = self.get_excel_cell('ontick', 'A:A')
        self.index_column =  {key: i + 1 for i, key in enumerate(self.index_column_arr)}
        # print ("===========" +str(self.index_column_dict))


        self.dwx = dwx_client(self, MT4_directory_path, sleep_delay, max_retry_command_seconds, verbose=verbose)
        sleep(1)

        self.dwx.start()

        # account information is stored in self.dwx.account_info.
        print("Account info:", self.dwx.account_info)

        # subscribe to tick data:
        self.dwx.subscribe_symbols([ 'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADJPY', 'EURAUD', 'EURCAD', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
])
        # self.dwx.subscribe_symbols([])

        # subscribe to bar data:
        self.dwx.subscribe_symbols_bar_data([['EURUSD', 'M1'], ['GBPJPY', 'M1'], ['AUDCAD', 'M1']])
        # self.dwx.subscribe_symbols_bar_data([])

        # request historic data:
        end = datetime.utcnow()
        start = end - timedelta(days=30)  # last 30 days
        # print(self.dwx.historic_data)
        self.dwx.get_historic_data('EURUSD', 'M15', start.timestamp(), end.timestamp())
        # print (self.dwx.historic_trades)
        # print(self.dwx.historic_data)


    def on_tick(self, symbol, bid, ask):
        now = datetime.utcnow()

        print('on_tick:', now, symbol, bid, ask)
        # self.update_excel_cell('onbar','A1',symbol)
        # self.update_excel_cell('onbar', 'B1', bid)
        # self.update_excel_cell('onbar', 'C1', ask)

        index_column = self.index_column # its a dict with keys as symbols and values as row numbers
        row_index = index_column.get(symbol)
        bid_address = f'B{row_index}'
        ask_address = f'C{row_index}'
        # for row in index_column:
        #     if row == symbol:
        #         row_index = index_column.index(row)  # Adding 1 to get the row number
        #         bid_address = f'B{row_index}'
        #         ask_address = f'C{row_index}'
        #         break
        if row_index:
            self.update_excel_cell('ontick', bid_address, bid)
            self.update_excel_cell('ontick', ask_address, ask)
            # print(f"Updated cell {cell_address} with value: {value}")
        else:
            print("Row Index name not found for the symbol "+symbol)

        # to test trading.
        # this will randomly try to open and close orders every few seconds.
        if self.open_test_trades:
            if now > self.last_open_time + timedelta(seconds=3):
                self.last_open_time = now

                order_type = 'buy'
                price = ask
                if random() > 0.5:
                    order_type = 'sell'
                    price = bid

                self.dwx.open_order(symbol=symbol, order_type=order_type, price=price, lots=0.5)

            if now > self.last_modification_time + timedelta(seconds=10):
                self.last_modification_time = now

                for ticket in self.dwx.open_orders.keys():
                    self.dwx.close_order(ticket, lots=0.1)

            if len(self.dwx.open_orders) >= 10:
                self.dwx.close_all_orders()  # self.dwx.close_orders_by_symbol('GBPUSD')  # self.dwx.close_orders_by_magic(0)

    def on_bar_data(self, symbol, time_frame, time, open_price, high, low, close_price, tick_volume):
        print('on_bar_data:', symbol, time_frame, datetime.utcnow(), time, open_price, high, low, close_price)

        # self.update_excel_cell('A1',symbol)
        # self.update_excel_cell('B1', time)
        # self.update_excel_cell('C1', open_price)
        # self.update_excel_cell('D1', high)
        # self.update_excel_cell('E1', low)
        # self.update_excel_cell('F1', close_price)


    def on_historic_data(self, symbol, time_frame, data):
        # you can also access the historic data via self.dwx.historic_data.
        print('historic_data:', symbol, time_frame, f'{len(data)} bars')

    def on_historic_trades(self):
        print(f'historic_trades: {len(self.dwx.historic_trades)}')

    def on_message(self, message):
        if message['type'] == 'ERROR':
            print(message['type'], '|', message['error_type'], '|', message['description'])
        elif message['type'] == 'INFO':
            print(message['type'], '|', message['message'])

    # triggers when an order is added or removed, not when only modified.
    def on_order_event(self):
        print(f'on_order_event. open_orders: {len(self.dwx.open_orders)} open orders')

    def update_excel_cell(self, sheet_name , cell, value, file_path=file_path):
        # Connect to an existing workbook
        wb = xw.Book(file_path)
        # Select the sheet
        sheet = wb.sheets[sheet_name]
        # Update the cell value
        sheet.range(cell).value = value

    def get_excel_cell(self, sheet_name , cell, file_path=file_path):
        # Connect to an existing workbook
        wb = xw.Book(file_path)
        # Select the sheet
        sheet = wb.sheets[sheet_name]
        # Get the cell value
        value = sheet.range(cell).value
        return value

MT4_files_dir = 'C:/Users/Kalyan/AppData/Roaming/MetaQuotes/Terminal/51337600F56B69473E15EAFB8A7586B4/MQL4/Files/'

processor = tick_processor(MT4_files_dir)
# print(processor.get_excel_cell('A1'))





while processor.dwx.ACTIVE:
    sleep(1)

