# from slacker import Slacker
#
# slacker = Slacker('xoxb-2143616568480-2119135848069-KcB9662VZp2pTJCW1CmUeR8g')
#
# slacker.chat.post_message('#stockanalitics','hello')

# from stock_mysql import setting
# import pandas as pd
# conn = setting.connect_db()
# table_stock_code = setting.fetch_stock_code_where_code(conn, 'A005930')
# table_stock_code = pd.DataFrame(table_stock_code)
# print(table_stock_code)

import multiprocessing as mp
import subprocess
import numpy as np
import pandas as pd
x = np.array([0.1,0.2,0.3,0.5,0.4,0.7])
from stock_mysql import setting
conn = setting.connect_db()

# print(b)
# print(range(len(b)))
# # b = b.reindex(range(len(b)))
# # b = b.reindex()
# # print(type(b))
# print(b)
# # print(x)
# # print(x[-3:])

# # print(h)

# print(len(b)-3)
# print(b.loc[len(b)-3,'now'])
# exit()
def target_list(n):
    data = setting.fetch_all_stock_code(conn)
    data = pd.DataFrame(data)
    sort = np.argsort(data['pct'])
    sort_data = data.loc[sort.tolist(), :]
    sort_data = sort_data.reset_index()
    while True:
        if sort_data.loc[len(sort_data) - n, 'pct'] <=0:
            n = n-1
            continue
        break
    h = sum(sort_data['pct'][-n:])
    invest_list = []
    for list_num in range(len(data)-n):
        invest_list.append(0)
    for list_num in range(n):
        pct = sort_data.loc[len(sort_data) - n + list_num, 'pct'] / h
        if pct <= 0:
            invest_list.append(0)
            continue
        invest_list.append(pct)
    sort_data['invest_pct'] = invest_list
    for count in range(len(data)):
        setting.update_stock_code(conn,sort_data['code'][count],float(sort_data['invest_pct'][count]))
sort_data=target_list(4)

# buy_percent = sort_data[['code','invest_pct']].to_dict()
# buy_percent2 = {key: value for key, value in dict.fromkeys(sort_data[['code','invest_pct']]).items()}
# print(buy_percent2)
# print(buy_percent['invest_pct'][5])
# def buy_amount_code(code):
#     data = setting.fetch_all_stock_code(conn)
#     sort_data = data[['code', 'invest_pct']].to_dict('split')
#     for count in range(len(data)):
#         if sort_data['data'][count][0] == code:
#             print(sort_data['data'][count][1])
# #
# data = setting.fetch_all_stock_code(conn)
# data = pd.DataFrame(data)
# print(f'{data[["code"]]} == > {data[["pct"]]*2}')
# subprocess.call(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe'])  # 모델 생성
# def model_process():
# subprocess.call(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_model_preprocess/stock_model_preprocess.exe'])  # 모델 제작 전처리
# import os
# os.popen('C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe')
# os.system('C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe')
# subprocess.call(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe'])  # 모델 생성
# p = mp.Process(name='model_make_Process',target=model_process())
# p.start()
import ctypes
# ctypes.windll.shell32.ShellExecuteA(0,’open’,'C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe',None,None,1)
