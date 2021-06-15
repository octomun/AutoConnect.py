import sys
from PyQt5.QtWidgets import *
import win32com.client
import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta
import time
from stock_mysql import setting
conn = setting.connect_db()
fetch = setting.fetch_all_stock_code(conn)
fetch = pd.DataFrame(fetch)
print(fetch)
code = fetch['code']
os.chdir('F:/stock')
for i in range(len(fetch)):
    try :
        setting.drop_table(conn, code.values[i])
        setting.create_table(conn, code.values[i])
        time.sleep(0.2)
    except:
        setting.create_table(conn, code.values[i])
        time.sleep(0.2)

def RequestMT(code,j, dwm, st, et):
    # 연결 여부 체크
    print(code[j])
    g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
    g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    bConnect = g_objCpStatus.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False

    st_year = str(st)[:4]
    st_month = str(st)[5:7]
    st_day = str(st)[-2:]
    st = datetime.date(int(st_year),int(st_month),int(st_day))

    if st > et:
        t = st
        st = et
        et = t
    est = et - relativedelta(years=1)
    while st.year != et.year:
        # est = et - relativedelta(years=1)
        objStockChart.SetInputValue(0, code[j])
        # objStockChart.SetInputValue(0, code)  # 종목코드
        objStockChart.SetInputValue(1, ord('1'))  # 1기간 2개수로 받기
        objStockChart.SetInputValue(2, to_integer(et)) #종료일
        objStockChart.SetInputValue(3, to_integer(est)) #시작일
        objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        objStockChart.SetInputValue(6, dwm)  # '차트 주기
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
            setting.insert_tabel(dates=dates, times=times,opens=opens,highs=highs, lows=lows,
                                 closes=closes,vols=vols,db =conn,db_name= code[j])
        et = et - relativedelta(years=1)
        est = et - relativedelta(years=1)
        time.sleep(0.5)
        print(et)
        print(est)
        print(len)


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

class check_model():
    for j in range(code.size):
        if os.path.isfile(f'{code[j]}.h5'):
            print(f'{code[j]} pass')
            continue
        RequestMT(code, j,ord('D'), 20100101,datetime.date.today()- relativedelta(days=1))
    import subprocess
    process = subprocess.run(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_model_preprocess/stock_model_preprocess.exe'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, stderr=subprocess.STDOUT) #모델 데이터 전처리
    #,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, stderr=subprocess.STDOUT
    # process.terminate()
    # process.wait()
    process = subprocess.run(['C:/Users/answl/Desktop/news_analy/stock/dist/stock_day_model/stock_day_model.exe'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, stderr=subprocess.STDOUT)
    #                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False,stderr=subprocess.STDOUT)  # 모델 생성
    # process.kill()
    print('clear model')