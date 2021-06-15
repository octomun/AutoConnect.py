import sys
from PyQt5.QtWidgets import *
from stock_mysql import setting
import win32com.client
import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta
import time
conn = setting.connect_db()
fetch = setting.fetch_all_stock_code(conn)
fetch = pd.DataFrame(fetch)
code = fetch['code']
print(code)
for i in range(len(fetch)):
    try :
        setting.drop_table_now(conn, code.values[i])
        setting.create_table_now(conn, code.values[i])
        time.sleep(0.2)
    except:
        setting.create_table_now(conn, code.values[i])
        time.sleep(0.2)



def RequestMT(code, dwm, et):
    for j in range(code.size):
        # 연결 여부 체크
        g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        objStockChart.SetInputValue(0, code[j])# 종목코드
        objStockChart.SetInputValue(1, ord('2'))  # 1기간 2개수로 받기
        objStockChart.SetInputValue(2, et) #종료일
        # objStockChart.SetInputValue(3, to_integer(est)) #시작일
        objStockChart.SetInputValue(4, 61)  # 조회 개수 1년
        objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 분/틱
        objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용

        objStockChart.BlockRequest2(1)

        rqStatus = objStockChart.GetDibStatus()
        rqRet = objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            print('rqstatus != 0')
            exit()

        len = objStockChart.GetHeaderValue(3) # 수신개수
        print('len = ', len)
        i=0
        for i in range(len):
            dates=(objStockChart.GetDataValue(0, i))
            times=(objStockChart.GetDataValue(1, i))
            opens=(objStockChart.GetDataValue(2, i))
            highs=(objStockChart.GetDataValue(3, i))
            lows=(objStockChart.GetDataValue(4, i))
            closes=(objStockChart.GetDataValue(5, i))
            vols=(objStockChart.GetDataValue(6, i))
            setting.insert_tabel_now(dates=dates, times=times, opens=opens, highs=highs, lows=lows,
                                 closes=closes, vols=vols, db=conn, db_name=code[j])
        time.sleep(0.5)

    return print(len)

today = datetime.date.today() - relativedelta(days=1)
if today.month < 10:
    month = '0' + str(today.month)
else:
    month = today.month
if today.day < 10:
    day = '0' + str(today.day)
else:
    day = today.day
today_date_minus = str(today.year) + str(month)+ str(day)

class Predict():
    RequestMT(code, ord('D'), today_date_minus)
    import subprocess
    process = subprocess.run(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_proprocess_day/stock_proprocess_day.exe'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, stderr=subprocess.STDOUT)  # 모델 사용 전처리
    # # process.wait()
    process = subprocess.run(['C:/Users/answl/Desktop/news_analy/stock/dist/prediction/prediction.exe'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, stderr=subprocess.STDOUT)  # 예측
    # process.kill()
    print('clear predict')
    # subprocess.run(['C:/Users/answl/Desktop/news_analy/stock/dist/prediction/prediction.exe'])
